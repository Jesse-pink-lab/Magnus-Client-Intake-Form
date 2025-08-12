from typing import Any, Dict, List, Optional
import json
import os
import sys
import subprocess
import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QTextEdit,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from .app import log_path, _log

from .pages import PAGES
from .state import STATE_FILE, load_state, save_state, build_default_state, migrate_state
from .renderer import PageRenderer
from .validation import (
    VALIDATORS,
    assets_held_away_errors,
    spouse_phone_errors,
    beneficiaries_ssn_errors,
)
from .home_page import HomePage
from .mru import get_mru, touch_mru, remove_from_mru

DRAFT_FILTER = "Magnus Draft (*.mgd)"
PDF_FILTER = "PDF Files (*.pdf)"
# PDF generator (optional)
try:
    from . import pdf_generator_reportlab as pdfgen
except Exception:
    pdfgen = None


class MagnusClientIntakeForm(QMainWindow):
    """Simple wizard driven by PAGES specification."""

    def __init__(self) -> None:
        super().__init__()
        self.state: Dict[str, Any] = load_state(STATE_FILE)
        self.current_page = -1
        self.pages: List[Dict[str, Any]] = []
        self.renderer = PageRenderer(self.state, VALIDATORS)
        self.current_path: Optional[str] = None
        self.session_active: bool = False
        self.is_dirty: bool = False
        self.last_invalid_fields: List[str] = []
        self.is_tearing_down: bool = False
        self.is_navigating: bool = False
        self.init_ui()
        self.init_menu()
        self.init_autosave()

    # ------------------------------------------------------------------ UI --
    def init_ui(self) -> None:
        self.setWindowTitle("Magnus Client Intake Form")
        self.resize(800, 600)

        self.root_stack = QStackedWidget()
        self.setCentralWidget(self.root_stack)

        # Home page
        self.home = HomePage()
        self.home.newRequested.connect(self.new_draft)
        self.home.openDialogRequested.connect(self.open_draft)
        self.home.openPathRequested.connect(self.open_draft_path)
        self.root_stack.addWidget(self.home)

        # Wizard container
        wizard = QWidget()
        root_layout = QVBoxLayout(wizard)
        root_layout.setContentsMargins(12, 8, 12, 8)
        root_layout.setSpacing(8)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        root_layout.addWidget(self.progress)

        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, 1)

        self.root_stack.addWidget(wizard)

        for index, page_spec in enumerate(PAGES):
            page_widget, meta = self.renderer.render_page_from_spec(
                page_spec, index, self.handle_field_change, self.on_next, self.on_back, self.go_home
            )
            self.stack.addWidget(page_widget)
            self.pages.append(meta)

        # Append Review page to the stack
        review = self._build_review_page()
        self.stack.addWidget(review)
        self.pages.append({"inputs": {}, "groups": [], "spec": {"sections": []}})

        self.update_progress()
        if self.pages:
            self.update_groups(0)
            self.validate_current_page(0)

    # ---------------------------------------------------------- NAVIGATION --
    def on_next(self) -> None:
        if self.is_tearing_down:
            return
        self.is_navigating = True
        try:
            # Run validation to update field highlighting but always allow navigation
            valid = self.validate_current_page(self.current_page)
            if not valid:
                fields = "\n".join(f"• {name}" for name in self.last_invalid_fields)
                if fields:
                    msg = (
                        "The following fields are missing or invalid:\n\n"
                        f"{fields}\n\n"
                        "You may continue, but please review before submitting."
                    )
                else:
                    msg = (
                        "Some fields on this page are missing or invalid.\n"
                        "You may continue, but please review before submitting."
                    )
                QMessageBox.warning(self, "Incomplete Information", msg)

            if self.current_page < len(self.pages) - 1:
                self.state.update(self.get_current_values(self.current_page))
                save_state(STATE_FILE, self.state)
                self.current_page += 1
                self.stack.setCurrentIndex(self.current_page)
                if self.current_page == len(self.pages) - 1:  # just entered Review
                    self._refresh_review()
                self.update_progress()
                if self.current_page < len(self.pages) - 1:
                    self.update_groups(self.current_page)
                    self.validate_current_page(self.current_page)
            else:
                # On Review page: finishing closes the window
                if hasattr(self, "autosave_timer"):
                    self.autosave_timer.stop()
                self.close()
        finally:
            self.is_navigating = False

    def on_back(self) -> None:
        if self.is_tearing_down:
            return
        self.is_navigating = True
        try:
            if self.current_page > 0:
                if self.current_page <= len(self.pages) - 1:
                    self.state.update(self.get_current_values(self.current_page))
                    save_state(STATE_FILE, self.state)
                self.current_page -= 1
                self.stack.setCurrentIndex(self.current_page)
                self.update_progress()
                if self.current_page < len(self.pages) - 1:
                    self.update_groups(self.current_page)
                    self.validate_current_page(self.current_page)
        finally:
            self.is_navigating = False

    def _build_review_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(12, 8, 12, 8)
        outer.setSpacing(8)

        title = QLabel("Review & Submit")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 700; margin: 6px 2px;")
        outer.addWidget(title)

        area = QScrollArea()
        area.setWidgetResizable(True)
        outer.addWidget(area, 1)

        inner = QWidget()
        area.setWidget(inner)
        v = QVBoxLayout(inner)

        self._review_text = QTextEdit()
        self._review_text.setReadOnly(True)
        self._review_text.setMinimumHeight(360)
        v.addWidget(self._review_text)

        row = QHBoxLayout()
        home_btn = QPushButton("Home")
        home_btn.clicked.connect(self.go_home)
        row.addWidget(home_btn)

        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.on_back)
        row.addWidget(back_btn)

        row.addStretch()

        save_btn = QPushButton("Save Draft")
        save_btn.clicked.connect(self.save_draft)
        row.addWidget(save_btn)

        gen_btn = QPushButton("Generate PDF Report")
        gen_btn.clicked.connect(self._generate_pdf)
        row.addWidget(gen_btn)

        outer.addLayout(row)
        return page

    def _refresh_review(self) -> None:
        def get(name: str, default: str = "Not provided") -> str:
            val = self.state.get(name)
            if val is True:
                return "Yes"
            if val is False:
                return "No"
            return val if (val not in ("", None)) else default
        investment_objective = get("investment_objective")
        time_horizon = get("time_horizon")
        assets_total = get("assets_held_away_total")
        assets_liquid = get("assets_held_away_liquid")
        assets_other = get("assets_held_away_other_brokers")

        # Dependents
        dependents = self.state.get("dependents") or []
        if not dependents and any(
            self.state.get(k) for k in ("dep_full_name", "dep_dob", "dep_relationship")
        ):
            dependents = [
                {
                    "name": self.state.get("dep_full_name"),
                    "dob": self.state.get("dep_dob"),
                    "relationship": self.state.get("dep_relationship"),
                }
            ]
        dep_lines = [
            f"{d.get('full_name', 'Not provided')} (DOB: {d.get('dob', 'Not provided')}, Relationship: {d.get('relationship', 'Not provided')})"
            for d in dependents
        ]
        dependents_html = "<br/>".join(dep_lines) if dep_lines else "Not provided"

        # Beneficiaries
        beneficiaries = self.state.get("beneficiaries") or []
        if not beneficiaries and any(
            self.state.get(k)
            for k in ("ben_full_name", "ben_dob", "ben_relationship", "ben_allocation_pct")
        ):
            beneficiaries = [
                {
                    "full_name": self.state.get("ben_full_name"),
                    "dob": self.state.get("ben_dob"),
                    "relationship": self.state.get("ben_relationship"),
                    "allocation": self.state.get("ben_allocation_pct"),
                }
            ]
        ben_lines = [
            f"{b.get('full_name', 'Not provided')} (DOB: {b.get('dob', 'Not provided')}, Relationship: {b.get('relationship', 'Not provided')}, SSN: {b.get('beneficiary_ssn', 'Not provided')}, Allocation: {b.get('allocation', 'Not provided')})"
            for b in beneficiaries
        ]
        beneficiaries_html = "<br/>".join(ben_lines) if ben_lines else "Not provided"

        # Investment experience
        asset_map = [
            ("Stocks", "stocks"),
            ("Bonds", "bonds"),
            ("Mutual Funds", "mutual_funds"),
            ("UITs", "uits"),
            ("Annuities (Fixed)", "annuities_fixed"),
            ("Annuities (Variable)", "annuities_variable"),
            ("Options", "options"),
            ("Commodities", "commodities"),
            ("Alternative Investments", "alternative_investments"),
            ("Limited Partnerships", "limited_partnerships"),
            ("Variable Contracts", "variable_contracts"),
        ]
        exp_lines = []
        for label, key in asset_map:
            year = get(f"{key}_year_started")
            level = get(f"{key}_level")
            if year == "Not provided" and level == "Not provided":
                continue
            exp_lines.append(
                f"{label} – Year Started: {year}, Level: {level}"
            )
        investment_experience = "<br/>".join(exp_lines) if exp_lines else "Not provided"

        # Spouse/partner info
        if not self.state.get("no_spouse"):
            spouse_html = (
                f"<b>Full Name:</b> {get('spouse_full_name')}<br/>"
                f"<b>Date of Birth:</b> {get('spouse_dob')}<br/>"
                f"<b>SSN:</b> {get('spouse_ssn')}<br/>"
                f"<b>Employment Status:</b> {get('spouse_employment_status')}<br/>"
                f"<b>Employer:</b> {get('spouse_employer_name')}<br/>"
                f"<b>Job Title:</b> {get('spouse_job_title')}<br/>"
                f"<b>Phone:</b> {get('spouse_phone')}"
            )
        else:
            spouse_html = "[Not applicable]"

        html = f"""
        <div style="font-family: Segoe UI,Inter,system-ui; color:#111827;">
          <h3>— MAGNUS CLIENT INTAKE FORM — REVIEW —</h3>

          <h4>PERSONAL INFORMATION</h4>
          <p>
            <b>Full Name:</b> {get('full_name')}<br/>
            <b>Date of Birth:</b> {get('dob')}<br/>
            <b>SSN:</b> {get('ssn')}<br/>
            <b>Citizenship:</b> {get('citizenship_status')}<br/>
            <b>Marital Status:</b> {get('marital_status')}
          </p>

          <h4>CONTACT INFORMATION</h4>
          <p>
            <b>Residential Address:</b> {get('address')}<br/>
            <b>Email:</b> {get('email')}<br/>
            <b>Home Phone:</b> {get('phone_home')}<br/>
            <b>Mobile Phone:</b> {get('phone_mobile')}<br/>
            <b>Work Phone:</b> {get('phone_work')}
          </p>

          <h4>EMPLOYMENT INFORMATION</h4>
          <p>
            <b>Status:</b> {get('employment_status')}<br/>
            <b>Employer:</b> {get('employer_name')}<br/>
            <b>Title:</b> {get('job_title')}<br/>
            <b>Years with Employer:</b> {get('years_with_employer')}
          </p>

          <h4>FINANCIAL INFORMATION</h4>
          <p>
            <b>Education:</b> {get('education')}<br/>
            <b>Risk Tolerance:</b> {get('risk_tolerance')}<br/>
            <b>Time Horizon:</b> {time_horizon}<br/>
            <b>Investment Objective:</b> {investment_objective}<br/>
            <b>Est. Net Worth:</b> {get('est_net_worth')}<br/>
            <b>Est. Liquid Net Worth:</b> {get('est_liquid_net_worth')}<br/>
            <b>Assets Held Away – Total:</b> {assets_total}<br/>
            <b>Assets Held Away – Liquid:</b> {assets_liquid}<br/>
            <b>Assets Held Away – Other Brokerage Firms:</b> {assets_other}
          </p>

          <h4>SPOUSE/PARTNER INFORMATION</h4>
          <p>{spouse_html}</p>

          <h4>DEPENDENTS</h4>
          <p>{dependents_html}</p>

          <h4>BENEFICIARIES</h4>
          <p>{beneficiaries_html}</p>

          <h4>INVESTMENT EXPERIENCE</h4>
          <p>{investment_experience}</p>

          <h4>TRUSTED CONTACT</h4>
          <p>
            <b>Name:</b> {get('tcp_full_name')}<br/>
            <b>Relationship:</b> {get('tcp_relationship')}<br/>
            <b>Phone:</b> {get('tcp_phone')}<br/>
            <b>Email:</b> {get('tcp_email')}
          </p>

          <h4>REGULATORY (highlights)</h4>
          <p>
            <b>Electronic Delivery Consent:</b> {get('ed_consent')}<br/>
            <b>Employee of this BD:</b> {get('employee_this_bd')}<br/>
            <b>SRO Member:</b> {get('sro_member')}<br/>
            <b>Foreign FI Account:</b> {get('has_ffi')}<br/>
            <b>PEP:</b> {get('is_pep')}
          </p>
        </div>
        """
        self._review_text.setHtml(html)


    def _suggest_pdf_name(self) -> str:
        name = self.state.get("full_name") or "Client"
        date = datetime.date.today().strftime("%Y-%m-%d")
        return f"{name} - Magnus Intake {date}"

    def pick_save_pdf_path(self, suggested_name: str) -> str | None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            str(self.default_drafts_dir() / f"{suggested_name}.pdf"),
            PDF_FILTER,
        )
        if not path:
            return None
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        return path

    def _generate_pdf(self) -> None:
        if pdfgen is None or not hasattr(pdfgen, "generate"):
            QMessageBox.warning(self, "PDF", "PDF generator module not available.")
            return
        suggested = self._suggest_pdf_name()
        path = self.pick_save_pdf_path(suggested)
        if not path:
            return
        try:
            pdfgen.generate(self.state, path)
            QMessageBox.information(self, "PDF", f"PDF generated successfully:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "PDF Error", f"Failed to generate PDF:\n{e}")

    def update_progress(self) -> None:
        total = len(self.pages)
        pct = round(((self.current_page + 1) / total) * 100) if total else 0
        self.progress.setValue(pct)

    # ----------------------------------------------------------- SESSION --
    def mark_dirty(self) -> None:
        self.is_dirty = True

    def start_session(self) -> None:
        self.session_active = True
        self.is_dirty = False
        self.current_page = 0 if self.pages else -1
        self.autosave_timer.start(60000)

    def end_session(self) -> None:
        self.session_active = False
        self.is_dirty = False
        self.current_path = None
        self.autosave_timer.stop()

    def maybe_discard(self) -> bool:
        """Return True if navigation can proceed."""
        if not self.session_active or not self.is_dirty:
            return True
        resp = QMessageBox.question(
            self,
            "Discard changes?",
            "Discard unsaved changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return resp == QMessageBox.StandardButton.Yes

    # ------------------------------------------------------------- VALUES --
    def get_current_values(self, index: int) -> Dict[str, Any]:
        if index < 0 or index >= len(self.pages):
            return {}
        meta = self.pages[index]
        values: Dict[str, Any] = {}
        for name, info in meta["inputs"].items():
            ftype = info["type"]
            if ftype == "radio":
                btn = info["group"].checkedButton()
                values[name] = btn.text() if btn else ""
            elif ftype == "repeating_group":
                values[name] = self.state.get(name, [])
            elif ftype == "select":
                values[name] = info["widget"].currentText()
            elif ftype in ("text", "number"):
                values[name] = info["widget"].text()
            elif ftype == "date":
                values[name] = info["widget"].date().toString("yyyy-MM-dd")
            elif ftype == "textarea":
                values[name] = info["widget"].toPlainText()
            elif ftype == "checkbox":
                values[name] = info["widget"].isChecked()
        return values

    # -------------------------------------------------------------- GROUPS --
    def update_groups(self, index: int) -> None:
        meta = self.pages[index]
        values = self.get_current_values(index)
        for widget, cond in meta["groups"]:
            name, expected = next(iter(cond.items()))
            widget.setVisible(values.get(name, "") == expected)

    # ----------------------------------------------------------- VALIDATE --
    def validate_current_page(self, index: int) -> bool:
        meta = self.pages[index]
        values = self.get_current_values(index)
        merged = dict(self.state)
        merged.update(values)
        inputs = meta.get("inputs", {})
        invalid_fields: List[str] = []
        valid = True

        for section in meta["spec"].get("sections", []):
            for field in self.renderer.iterate_fields(section.get("fields", []), merged):
                name = field.get("name")
                label = field.get("label", name)
                rg = field.get("_rg")
                if rg:
                    grp = rg["name"]
                    i = rg["index"]
                    value = merged.get(grp, [])
                    if isinstance(value, list) and i < len(value):
                        value = value[i].get(name, "")
                    else:
                        value = ""
                    label = f"{label} {i + 1}"
                else:
                    value = values.get(name, "")
                if field.get("required"):
                    if field["type"] == "checkbox":
                        if not value:
                            valid = False
                            invalid_fields.append(label)
                    elif not value:
                        valid = False
                        invalid_fields.append(label)
                if field.get("validate") and value not in ("", False):
                    validator = VALIDATORS.get(field["validate"])
                    if validator:
                        ok = True
                        try:
                            try:
                                ok = validator(value, merged)
                            except TypeError:
                                ok = validator(value)
                        except Exception as e:
                            from .app import _log
                            _log(f"Validator error {field.get('name')}: {e}")
                            ok = False
                        if not ok:
                            valid = False
                            invalid_fields.append(label)

        if {"est_net_worth", "est_liquid_net_worth"}.issubset(inputs.keys()):
            try:
                if not VALIDATORS["liquid_lte_net"]("", merged):
                    valid = False
                    invalid_fields.append("Liquid Net Worth vs Net Worth")
            except Exception as e:
                from .app import _log
                _log(f"Validator error liquid_lte_net: {e}")
                valid = False
                invalid_fields.append("Liquid Net Worth vs Net Worth")
        assets_fields = {
            "assets_held_away_total",
            "assets_held_away_liquid",
            "assets_held_away_other_brokers",
        }
        if assets_fields & inputs.keys():
            for msg in assets_held_away_errors(merged):
                valid = False
                invalid_fields.append(msg)
        for msg in spouse_phone_errors(merged):
            valid = False
            invalid_fields.append(msg)
        if "beneficiaries" in inputs:
            try:
                if not VALIDATORS["beneficiaries_sum_100"]("", merged):
                    valid = False
                    invalid_fields.append("Beneficiaries Allocation Total")
            except Exception as e:
                from .app import _log
                _log(f"Validator error beneficiaries_sum_100: {e}")
                valid = False
                invalid_fields.append("Beneficiaries Allocation Total")
            for msg in beneficiaries_ssn_errors(merged.get("beneficiaries") or []):
                valid = False
                invalid_fields.append(msg)

        meta["next_btn"].setEnabled(True)
        self.last_invalid_fields = invalid_fields
        return valid

    # ------------------------------------------------------------- SIGNAL --
    def handle_field_change(self) -> None:
        if self.is_tearing_down or self.is_navigating:
            return
        self.state.update(self.get_current_values(self.current_page))
        self.mark_dirty()
        self.update_groups(self.current_page)
        self.validate_current_page(self.current_page)

    # --------------------------------------------------------------- MENU --
    def init_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")

        new_act = QAction("New Draft", self)
        new_act.triggered.connect(self.new_draft)
        file_menu.addAction(new_act)

        open_act = QAction("Open…", self)
        open_act.triggered.connect(self.open_draft)
        file_menu.addAction(open_act)

        home_act = QAction("Home", self)
        home_act.setShortcut("Ctrl+H")
        home_act.triggered.connect(self.go_home)
        file_menu.addAction(home_act)

        save_act = QAction("Save", self)
        save_act.triggered.connect(self.save_draft)
        file_menu.addAction(save_act)

        save_as_act = QAction("Save As…", self)
        save_as_act.triggered.connect(self.save_draft_as)
        file_menu.addAction(save_as_act)

        file_menu.addSeparator()

        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        help_menu = self.menuBar().addMenu("&Help")
        act_log = QAction("Open Crash Log Folder", self)

        def _open_log_dir() -> None:
            p = str(log_path().parent)
            _log(f"[UI] Open log dir {p}")
            try:
                if sys.platform.startswith("win"):
                    os.startfile(p)  # type: ignore
                elif sys.platform == "darwin":
                    subprocess.check_call(["open", p])
                else:
                    subprocess.check_call(["xdg-open", p])
            except Exception as e:
                QMessageBox.information(
                    self, "Crash log", f"Crash logs live in:\n{p}\n\n{e}"
                )

        help_menu.addAction(act_log)
        act_log.triggered.connect(_open_log_dir)

    # ----------------------------------------------------------- AUTOSAVE --
    def init_autosave(self) -> None:
        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(60000)
        self.autosave_timer.timeout.connect(self.autosave_tick)

    def autosave_tick(self) -> None:
        if (
            self.is_tearing_down
            or not self.session_active
            or self.current_page < 0
            or self.current_page >= len(self.pages)
            or not self.current_path
        ):
            return
        try:
            self.state.update(self.get_current_values(self.current_page))
            save_state(self.current_path, self.state)
        except Exception as e:
            _log(f"AUTOSAVE ERROR: {e}")

    # ------------------------------------------------------------ DRAFTS --
    def default_drafts_dir(self) -> Path:
        if sys.platform.startswith("win"):
            base = Path(os.environ.get("APPDATA") or Path.home())
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".local" / "share"
        path = base / "Magnus" / "Drafts"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def pick_save_draft_path(self) -> str | None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Draft",
            str(self.default_drafts_dir()),
            DRAFT_FILTER,
        )
        if not path:
            return None
        if not path.lower().endswith(".mgd"):
            path += ".mgd"
        return path

    def pick_open_draft_path(self) -> str | None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Draft",
            str(self.default_drafts_dir()),
            DRAFT_FILTER,
        )
        return path or None

    def do_save(self, path: str) -> bool:
        if not path:
            return False
        try:
            save_state(path, self.state)
            self.current_path = path
            self.is_dirty = False
            touch_mru(path)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Save failed", f"Could not save file:\n{e}")
            return False

    def save_draft(self, auto: bool = False) -> None:
        if (
            not self.session_active
            or self.current_page < 0
            or self.current_page >= len(self.pages)
        ):
            return
        self.state.update(self.get_current_values(self.current_page))
        if auto:
            if self.current_path:
                self.do_save(self.current_path)
            return
        if self.current_path:
            if self.do_save(self.current_path):
                QMessageBox.information(
                    self, "Save Draft", f"Draft saved:\n{self.current_path}"
                )
        else:
            path = self.pick_save_draft_path()
            if path and self.do_save(path):
                QMessageBox.information(
                    self, "Save Draft", f"Draft saved:\n{path}"
                )

    def save_draft_as(self) -> None:
        path = self.pick_save_draft_path()
        if path:
            self.state.update(self.get_current_values(self.current_page))
            if self.do_save(path):
                QMessageBox.information(self, "Save Draft", f"Draft saved:\n{path}")

    def open_draft(self) -> None:
        if self.session_active and not self.maybe_discard():
            return
        path = self.pick_open_draft_path()
        if path:
            self.open_draft_path(path)

    def new_draft(self) -> None:
        if self.session_active and not self.maybe_discard():
            return
        self.autosave_timer.stop()
        self.state = build_default_state()
        self.current_path = None
        self.rebuild_pages()
        self.start_session()
        self.show_wizard()

    def rebuild_pages(self) -> None:
        self.is_tearing_down = True
        try:
            while self.stack.count():
                w = self.stack.widget(0)
                self.stack.removeWidget(w)
                w.deleteLater()
            self.pages.clear()
            self.renderer = PageRenderer(self.state, VALIDATORS)
            for index, page_spec in enumerate(PAGES):
                page_widget, meta = self.renderer.render_page_from_spec(
                    page_spec, index, self.handle_field_change, self.on_next, self.on_back, self.go_home
                )
                self.stack.addWidget(page_widget)
                self.pages.append(meta)
            review = self._build_review_page()
            self.stack.addWidget(review)
            self.pages.append({"inputs": {}, "groups": [], "spec": {"sections": []}})
            self.current_page = 0 if self.pages else -1
            self.stack.setCurrentIndex(0)
            self.update_progress()
            if self.pages:
                self.update_groups(0)
                self.validate_current_page(0)
        finally:
            self.is_tearing_down = False

    # -------------------------------------------------------------- HOME/WIZARD --
    def show_home(self) -> None:
        self.home.refresh(get_mru())
        self.root_stack.setCurrentWidget(self.home)

    def show_wizard(self) -> None:
        self.root_stack.setCurrentIndex(1)

    def go_home(self) -> None:
        if not self.maybe_discard():
            return
        self.autosave_timer.stop()
        self.end_session()
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.pages.clear()
        self.current_page = -1
        self.show_home()

    def open_draft_path(self, path: str) -> None:
        self.autosave_timer.stop()
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            for page in PAGES:
                for section in page.get("sections", []):
                    for field in section.get("fields", []):
                        if field.get("type") == "repeating_group":
                            name = field.get("name")
                            val = data.get(name)
                            if isinstance(val, list):
                                data[name] = [v for v in val if isinstance(v, dict)]
                            else:
                                data[name] = []
            self.state = migrate_state(data)
            self.current_path = path
            self.rebuild_pages()
            invalid = 0
            for i in range(len(self.pages) - 1):
                if not self.validate_current_page(i):
                    invalid = i
                    break
            self.current_page = invalid
            self.stack.setCurrentIndex(invalid)
            self.update_progress()
            if invalid < len(self.pages) - 1:
                self.update_groups(invalid)
                self.validate_current_page(invalid)
            touch_mru(path)
            self.start_session()
            self.show_wizard()
        except Exception as e:
            QMessageBox.critical(self, "Open Draft", f"Failed to open draft:\n{e}")
            remove_from_mru(path)
            self.end_session()
            self.show_home()

    # -------------------------------------------------------------- CLOSE --
    def closeEvent(self, event) -> None:  # type: ignore[override]
        if self.session_active and not self.maybe_discard():
            event.ignore()
            return
        event.accept()
