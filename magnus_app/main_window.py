from typing import Any, Dict, List

from PyQt6.QtWidgets import (
    QHBoxLayout, QMainWindow, QProgressBar, QPushButton, QStackedWidget,
    QVBoxLayout, QWidget, QScrollArea, QTextEdit, QLabel, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from .pages import PAGES
from .state import STATE_FILE, load_state, save_state
from .renderer import PageRenderer
from .validation import VALIDATORS
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
        self.current_page = 0
        self.pages: List[Dict[str, Any]] = []
        self.renderer = PageRenderer(self.state, VALIDATORS)
        self.init_ui()

    # ------------------------------------------------------------------ UI --
    def init_ui(self) -> None:
        self.setWindowTitle("Magnus Client Intake Form")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        root_layout.addWidget(self.progress)

        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, 1)

        for index, page_spec in enumerate(PAGES):
            page_widget, meta = self.renderer.render_page_from_spec(
                page_spec, index, self.handle_field_change, self.on_next, self.on_back
            )
            self.stack.addWidget(page_widget)
            self.pages.append(meta)

        # Append Review page to the stack
        review = self._build_review_page()
        self.stack.addWidget(review)

        self.update_progress()
        self.update_groups(0)
        self.validate_current_page(0)

    # ---------------------------------------------------------- NAVIGATION --
    def on_next(self) -> None:
        # still inside form pages
        if self.current_page < len(self.pages):
            if not self.validate_current_page(self.current_page):
                return
            self.state.update(self.get_current_values(self.current_page))
            save_state(STATE_FILE, self.state)
            self.current_page += 1
            self.stack.setCurrentIndex(self.current_page)
            if self.current_page == len(self.pages):  # just entered Review
                self._refresh_review()
            self.update_progress()
            if self.current_page < len(self.pages):
                self.update_groups(self.current_page)
                self.validate_current_page(self.current_page)
        else:
            # On Review page: buttons handle actions
            pass

    def on_back(self) -> None:
        if self.current_page > 0:
            if self.current_page <= len(self.pages) - 1:
                self.state.update(self.get_current_values(self.current_page))
                save_state(STATE_FILE, self.state)
            self.current_page -= 1
            self.stack.setCurrentIndex(self.current_page)
            self.update_progress()
            if self.current_page < len(self.pages):
                self.update_groups(self.current_page)
                self.validate_current_page(self.current_page)

    def _build_review_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0,0,0,0)

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
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.on_back)
        row.addWidget(back_btn)

        row.addStretch()

        save_btn = QPushButton("Save Draft")
        save_btn.clicked.connect(lambda: save_state(STATE_FILE, self.state))
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

        def join_options(options):
            selected = [label for key, label in options if self.state.get(key)]
            return ", ".join(selected) if selected else "Not provided"

        # Investment purpose checkboxes
        purposes = join_options([
            ("inv_purpose_income", "Income"),
            ("inv_purpose_growth_income", "Growth and Income"),
            ("inv_purpose_cap_app", "Capital Appreciation"),
            ("inv_purpose_speculation", "Speculation"),
        ])

        # Investment objectives rankings
        objectives_map = [
            ("obj_trading_profits_rank", "Trading Profits"),
            ("obj_speculation_rank", "Speculation"),
            ("obj_capital_app_rank", "Capital Appreciation"),
            ("obj_income_rank", "Income"),
            ("obj_preservation_rank", "Preservation of Capital"),
        ]
        obj_lines = [
            f"{label}: {get(key)}" for key, label in objectives_map if self.state.get(key)
        ]
        objectives = "<br/>".join(obj_lines) if obj_lines else "Not provided"

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
            f"{d.get('name', 'Not provided')} (DOB: {d.get('dob', 'Not provided')}, Relationship: {d.get('relationship', 'Not provided')})"
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
                    "name": self.state.get("ben_full_name"),
                    "dob": self.state.get("ben_dob"),
                    "relationship": self.state.get("ben_relationship"),
                    "percentage": self.state.get("ben_allocation_pct"),
                }
            ]
        ben_lines = [
            f"{b.get('name', 'Not provided')} (DOB: {b.get('dob', 'Not provided')}, Relationship: {b.get('relationship', 'Not provided')}, Allocation: {b.get('percentage', 'Not provided')})"
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
                f"<b>Job Title:</b> {get('spouse_job_title')}"
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
            <b>Investment Purpose:</b> {purposes}<br/>
            <b>Investment Objectives:</b><br/>{objectives}<br/>
            <b>Est. Net Worth:</b> {get('est_net_worth')}<br/>
            <b>Est. Liquid Net Worth:</b> {get('est_liquid_net_worth')}<br/>
            <b>Assets Held Away:</b> {get('assets_held_away')}
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
            <b>Electronic Delivery Consent:</b> {get('electronic_delivery_consent')}<br/>
            <b>Employee of this BD:</b> {get('employee_this_bd')}<br/>
            <b>SRO Member:</b> {get('sro_member')}<br/>
            <b>Foreign FI Account:</b> {get('has_ffi')}<br/>
            <b>PEP:</b> {get('is_pep')}
          </p>
        </div>
        """
        self._review_text.setHtml(html)

    
    def _generate_pdf(self) -> None:
        if pdfgen is None or not hasattr(pdfgen, "generate"):
            QMessageBox.warning(self, "PDF", "PDF generator module not available.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "Magnus_Client_Intake_Form.pdf", "PDF Files (*.pdf)"
        )
        if not path:
            return
        try:
            pdfgen.generate(self.state, path)
            QMessageBox.information(self, "PDF", f"PDF generated successfully:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "PDF Error", f"Failed to generate PDF:\n{e}")

    def update_progress(self) -> None:
        total = len(self.pages) + 1  # +1 for Review page
        pct = round(((self.current_page + 1) / total) * 100)
        self.progress.setValue(pct)

    # ------------------------------------------------------------- VALUES --
    def get_current_values(self, index: int) -> Dict[str, Any]:
        meta = self.pages[index]
        values: Dict[str, Any] = {}
        for name, info in meta["inputs"].items():
            ftype = info["type"]
            if ftype == "radio":
                btn = info["group"].checkedButton()
                values[name] = btn.text() if btn else ""
            elif ftype == "repeating_group":
                items = []
                for sub_inputs in info.get("items", []):
                    item: Dict[str, Any] = {}
                    for uniq, sinfo in sub_inputs.items():
                        orig = sinfo.get("orig_name", uniq)
                        stype = sinfo["type"]
                        if stype == "radio":
                            btn = sinfo["group"].checkedButton()
                            val = btn.text() if btn else ""
                        elif stype == "select":
                            val = sinfo["widget"].currentText()
                        elif stype in ("text", "number"):
                            val = sinfo["widget"].text()
                        elif stype == "date":
                            val = sinfo["widget"].date().toString("yyyy-MM-dd")
                        elif stype == "textarea":
                            val = sinfo["widget"].toPlainText()
                        elif stype == "checkbox":
                            val = sinfo["widget"].isChecked()
                        else:
                            val = ""
                        item[orig] = val
                    # Only append if at least one field has data
                    if any(v not in ("", False) for v in item.values()):
                        items.append(item)
                values[name] = items
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
        valid = True

        for section in meta["spec"].get("sections", []):
            for field in self.renderer.iterate_fields(section.get("fields", []), values):
                name = field.get("name")
                value = values.get(name, "")
                if field.get("required"):
                    if field["type"] == "checkbox":
                        if not value:
                            valid = False
                    elif not value:
                        valid = False
                if valid and field.get("validate") and value not in ("", False):
                    validator = VALIDATORS.get(field["validate"])
                    if validator:
                        try:
                            if not validator(value, values):
                                valid = False
                        except TypeError:
                            if not validator(value):
                                valid = False
                if not valid:
                    break
            if not valid:
                break

        meta["next_btn"].setEnabled(valid)
        return valid

    # ------------------------------------------------------------- SIGNAL --
    def handle_field_change(self) -> None:
        self.state.update(self.get_current_values(self.current_page))
        self.update_groups(self.current_page)
        self.validate_current_page(self.current_page)
