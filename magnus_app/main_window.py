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
        lines = ["---- MAGNUS CLIENT INTAKE FORM — REVIEW ----", ""]

        def get(name, default="Not provided"):
            val = self.state.get(name)
            if val is True:
                return "Yes"
            if val is False:
                return "No"
            return val if (val not in ("", None)) else default

        # Summarize key sections (add more fields as needed)
        lines += [
            "PERSONAL INFORMATION:",
            f"  Full Name: {get('full_name')}",
            f"  Date of Birth: {get('dob')}",
            f"  SSN: {get('ssn')}",
            f"  Marital Status: {get('marital_status')}",
            "",
            "CONTACT INFORMATION:",
            f"  Residential Address: {get('address')}",
            f"  Email: {get('email')}",
            f"  Mobile Phone: {get('phone_mobile')}",
            "",
            "EMPLOYMENT INFORMATION:",
            f"  Status: {get('employment_status')}",
            f"  Employer: {get('employer_name')}",
            f"  Title: {get('job_title')}",
            "",
            "FINANCIAL INFORMATION:",
            f"  Education: {get('education')}",
            f"  Risk Tolerance: {get('risk_tolerance')}",
            f"  Est. Net Worth: {get('est_net_worth')}",
            f"  Est. Liquid Net Worth: {get('est_liquid_net_worth')}",
            "",
            "TRUSTED CONTACT:",
            f"  Name: {get('tcp_full_name')}",
            f"  Phone: {get('tcp_phone')}",
            f"  Email: {get('tcp_email')}",
            "",
            "REGULATORY (highlights):",
            f"  Employee of this BD: {get('employee_this_bd')}",
            f"  SRO Member: {get('sro_member')}",
            f"  Foreign FI Account: {get('has_ffi')}",
            f"  PEP: {get('is_pep')}",
        ]
        self._review_text.setPlainText("\n".join(lines))

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
            pdfgen.generate(self.state, path)  # adjust only if your function name differs
            QMessageBox.information(self, "PDF", "PDF generated successfully.")
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
