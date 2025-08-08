#!/usr/bin/env python3
"""Data-driven wizard for the Magnus Client Intake Form.

This simplified PyQt implementation focuses on the regulatory portions of the
form.  The wizard is driven by a central ``PAGES`` specification which defines
pages, sections and fields.  Field widgets are generated at runtime and are
validated using validators from :mod:`validation`.
"""
from __future__ import annotations

import sys
from typing import Any, Dict, List, Tuple

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QProgressBar,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QTextEdit,
    QWidget,
    QSizePolicy,
    QSpacerItem,
)

from validation import VALIDATORS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ISO_COUNTRIES = [
    "United States",
    "Canada",
    "Mexico",
    "United Kingdom",
    "Germany",
    "France",
    "Australia",
    "Japan",
]

# ---------------------------------------------------------------------------
# Page specification
# ---------------------------------------------------------------------------
PAGES: List[Dict[str, Any]] = [
    {
        "key": "broker_dealer_relationships",
        "title": "Broker-Dealer Relationships",
        "sections": [
            {
                "title": "Associations",
                "fields": [
                    {
                        "name": "employee_this_bd",
                        "label": "Employee of this Broker-Dealer?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"employee_this_bd": "Yes"},
                        "fields": [
                            {
                                "name": "employee_name",
                                "label": "Employee Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "department",
                                "label": "Department",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "branch",
                                "label": "Branch",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "start_date",
                                "label": "Start Date",
                                "type": "date",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": "iso_date",
                            },
                        ],
                    },
                    {
                        "name": "related_this_bd",
                        "label": "Related to an Employee of this Broker-Dealer?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"related_this_bd": "Yes"},
                        "fields": [
                            {
                                "name": "related_employee_name",
                                "label": "Employee Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "relationship",
                                "label": "Relationship",
                                "type": "select",
                                "required": True,
                                "options": [
                                    "Spouse",
                                    "Parent",
                                    "Child",
                                    "Sibling",
                                    "Other",
                                ],
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "branch_related",
                                "label": "Branch",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                        ],
                    },
                    {
                        "name": "employee_other_bd",
                        "label": "Employee of another Broker-Dealer?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"employee_other_bd": "Yes"},
                        "fields": [
                            {
                                "name": "firm_name_other",
                                "label": "Firm Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "crd_other",
                                "label": "CRD #",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": "crd",
                            },
                            {
                                "name": "role_other",
                                "label": "Role",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "start_date_other",
                                "label": "Start Date",
                                "type": "date",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "iso_date",
                            },
                        ],
                    },
                    {
                        "name": "related_other_bd",
                        "label": "Related to an employee of another Broker-Dealer?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"related_other_bd": "Yes"},
                        "fields": [
                            {
                                "name": "firm_name_rel",
                                "label": "Firm Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "employee_name_rel",
                                "label": "Employee Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "relationship_rel",
                                "label": "Relationship",
                                "type": "select",
                                "required": True,
                                "options": [
                                    "Spouse",
                                    "Parent",
                                    "Child",
                                    "Sibling",
                                    "Other",
                                ],
                                "show_if": None,
                                "validate": None,
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        "key": "reg_affiliations",
        "title": "Regulatory Affiliations",
        "sections": [
            {
                "title": "SRO Membership & Control Persons",
                "fields": [
                    {
                        "name": "sro_member",
                        "label": "Member of Stk Exch./FINRA?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"sro_member": "Yes"},
                        "fields": [
                            {
                                "name": "membership_type",
                                "label": "Membership Type",
                                "type": "select",
                                "required": True,
                                "options": ["FINRA", "NYSE", "NASDAQ", "Other"],
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "sro_crd",
                                "label": "CRD #",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "crd",
                            },
                            {
                                "name": "sro_branch",
                                "label": "Branch",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                        ],
                    },
                    {
                        "name": "control_person",
                        "label": "Are you a senior officer, director, or 10% or more shareholder of a public company?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"control_person": "Yes"},
                        "fields": [
                            {
                                "name": "company_name",
                                "label": "Company Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "ticker",
                                "label": "Ticker",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "ticker",
                            },
                            {
                                "name": "exchange",
                                "label": "Exchange",
                                "type": "select",
                                "required": False,
                                "options": ["NYSE", "NASDAQ", "AMEX", "Other"],
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "role",
                                "label": "Role",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "ownership_pct",
                                "label": "Ownership %",
                                "type": "number",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "pct_0_100_two_dec",
                            },
                            {
                                "name": "as_of",
                                "label": "As Of",
                                "type": "date",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "iso_date",
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        "key": "foreign_accounts",
        "title": "Foreign Financial Accounts",
        "sections": [
            {
                "title": "FFI / Private Banking",
                "fields": [
                    {
                        "name": "has_ffi",
                        "label": "Foreign Financial Institution Account?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"has_ffi": "Yes"},
                        "fields": [
                            {
                                "name": "institution_name",
                                "label": "Institution Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "country",
                                "label": "Country",
                                "type": "select",
                                "required": True,
                                "options": "ISO_COUNTRIES",
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "purpose",
                                "label": "Purpose",
                                "type": "select",
                                "required": True,
                                "options": ["Savings", "Brokerage", "Payments", "Other"],
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "source_of_funds",
                                "label": "Source of Funds",
                                "type": "textarea",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "open_date",
                                "label": "Open Date",
                                "type": "date",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "iso_date",
                            },
                            {
                                "name": "private_banking",
                                "label": "Is this a private banking account?",
                                "type": "radio",
                                "required": False,
                                "options": ["Yes", "No"],
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "foreign_bank_acct",
                                "label": "Is this an account for a Foreign Bank?",
                                "type": "radio",
                                "required": False,
                                "options": ["Yes", "No"],
                                "show_if": None,
                                "validate": None,
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        "key": "pep",
        "title": "Politically Exposed Person (PEP)",
        "sections": [
            {
                "title": "PEP Screening",
                "fields": [
                    {
                        "name": "is_pep",
                        "label": "Politically Exposed Person?",
                        "type": "radio",
                        "required": True,
                        "options": ["Yes", "No"],
                    },
                    {
                        "type": "group",
                        "show_if": {"is_pep": "Yes"},
                        "fields": [
                            {
                                "name": "pep_name",
                                "label": "PEP Name",
                                "type": "text",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "pep_country",
                                "label": "Country",
                                "type": "select",
                                "required": True,
                                "options": "ISO_COUNTRIES",
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "pep_relationship",
                                "label": "Relationship",
                                "type": "select",
                                "required": True,
                                "options": ["Self", "Family", "Associate"],
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "pep_title",
                                "label": "Title",
                                "type": "text",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                            {
                                "name": "pep_start",
                                "label": "Start Date",
                                "type": "date",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "iso_date",
                            },
                            {
                                "name": "pep_end",
                                "label": "End Date",
                                "type": "date",
                                "required": False,
                                "options": None,
                                "show_if": None,
                                "validate": "iso_date>=pep_start",
                            },
                            {
                                "name": "pep_screening_consent",
                                "label": "I consent to screening",
                                "type": "checkbox",
                                "required": True,
                                "options": None,
                                "show_if": None,
                                "validate": None,
                            },
                        ],
                    },
                ],
            }
        ],
    },
]

# ---------------------------------------------------------------------------
# Helper functions for field iteration
# ---------------------------------------------------------------------------

def iterate_fields(fields: List[Dict[str, Any]], values: Dict[str, str]):
    """Yield field specs that should be validated based on ``show_if`` rules."""
    for fld in fields:
        if fld.get("type") == "group":
            cond = fld.get("show_if") or {}
            name, val = next(iter(cond.items()))
            if values.get(name, "") == val:
                yield from iterate_fields(fld["fields"], values)
        else:
            cond = fld.get("show_if")
            if cond:
                name, val = next(iter(cond.items()))
                if values.get(name, "") != val:
                    continue
            yield fld

# ---------------------------------------------------------------------------
# Main window implementation
# ---------------------------------------------------------------------------


class MagnusClientIntakeForm(QMainWindow):
    """Simple wizard driven by ``PAGES`` specification."""

    def __init__(self) -> None:
        super().__init__()
        self.state: Dict[str, str] = {}
        self.current_page = 0
        self.pages: List[Dict[str, Any]] = []
        self.init_ui()

    # ------------------------------------------------------------------ UI --
    def init_ui(self) -> None:
        self.setWindowTitle("Magnus Client Intake Form")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        root_layout.addWidget(self.progress)

        # Stacked widget for pages
        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, 1)

        for index, page_spec in enumerate(PAGES):
            page_widget, meta = self.render_page_from_spec(page_spec, index)
            self.stack.addWidget(page_widget)
            self.pages.append(meta)

        self.update_progress()
        self.update_groups(0)
        self.validate_current_page(0)

    # -------------------------------------------------------------- RENDER --
    def render_page_from_spec(self, page_spec: Dict[str, Any], index: int) -> Tuple[QWidget, Dict[str, Any]]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll, 1)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(content)

        inputs: Dict[str, Dict[str, Any]] = {}
        groups: List[Tuple[QWidget, Dict[str, str]]] = []

        # Sections
        for section in page_spec.get("sections", []):
            box = QGroupBox(section.get("title", ""))
            box_layout = QVBoxLayout(box)
            self.render_fields(section.get("fields", []), box_layout, inputs, groups)
            content_layout.addWidget(box)

        # Spacer to absorb extra height
        content_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Navigation buttons outside scroll area
        nav = QHBoxLayout()
        if index > 0:
            back_btn = QPushButton("Back")
            back_btn.clicked.connect(self.on_back)
            nav.addWidget(back_btn)
        nav.addStretch()
        if index < len(PAGES) - 1:
            next_btn = QPushButton("Next")
            next_btn.clicked.connect(self.on_next)
        else:
            next_btn = QPushButton("Finish")
            next_btn.clicked.connect(self.on_next)
        nav.addWidget(next_btn)
        layout.addLayout(nav)

        meta = {
            "spec": page_spec,
            "inputs": inputs,
            "groups": groups,
            "next_btn": next_btn,
        }
        return page, meta

    def render_fields(
        self,
        fields: List[Dict[str, Any]],
        layout: QVBoxLayout,
        inputs: Dict[str, Dict[str, Any]],
        groups: List[Tuple[QWidget, Dict[str, str]]],
    ) -> None:
        for field in fields:
            if field.get("type") == "group":
                container = QWidget()
                container_layout = QVBoxLayout(container)
                self.render_fields(field["fields"], container_layout, inputs, groups)
                layout.addWidget(container)
                groups.append((container, field["show_if"]))
                continue

            ftype = field.get("type")
            name = field.get("name")
            label_text = field.get("label", name)
            widget: QWidget

            if ftype == "radio":
                container = QWidget()
                hl = QHBoxLayout(container)
                lab = QLabel(label_text)
                lab.setWordWrap(True)
                hl.addWidget(lab)
                group = QButtonGroup(container)
                for opt in field.get("options", []):
                    rb = QRadioButton(opt)
                    group.addButton(rb)
                    hl.addWidget(rb)
                    rb.toggled.connect(self.handle_field_change)
                container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                inputs[name] = {"type": "radio", "group": group}
                layout.addWidget(container)
                continue

            if ftype == "select":
                widget = QComboBox()
                opts = field.get("options") or []
                if opts == "ISO_COUNTRIES":
                    opts = ISO_COUNTRIES
                widget.addItems([""] + opts)
                widget.currentTextChanged.connect(self.handle_field_change)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            elif ftype == "text":
                widget = QLineEdit()
                widget.textChanged.connect(self.handle_field_change)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            elif ftype == "number":
                widget = QLineEdit()
                widget.textChanged.connect(self.handle_field_change)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            elif ftype == "date":
                widget = QDateEdit()
                widget.setDisplayFormat("yyyy-MM-dd")
                widget.setCalendarPopup(True)
                widget.dateChanged.connect(self.handle_field_change)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            elif ftype == "textarea":
                widget = QTextEdit()
                widget.textChanged.connect(self.handle_field_change)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            elif ftype == "checkbox":
                widget = QCheckBox(label_text)
                widget.stateChanged.connect(self.handle_field_change)
                label_text = ""  # label already used
            else:
                continue

            if label_text:
                lab = QLabel(label_text)
                lab.setWordWrap(True)
                layout.addWidget(lab)
            layout.addWidget(widget)
            inputs[name] = {"type": ftype, "widget": widget}

    # ---------------------------------------------------------- NAVIGATION --
    def on_next(self) -> None:
        if not self.validate_current_page(self.current_page):
            return
        self.state.update(self.get_current_values(self.current_page))
        if self.current_page < len(PAGES) - 1:
            self.current_page += 1
            self.stack.setCurrentIndex(self.current_page)
            self.update_progress()
            self.update_groups(self.current_page)
            self.validate_current_page(self.current_page)
        else:
            self.close()

    def on_back(self) -> None:
        self.state.update(self.get_current_values(self.current_page))
        if self.current_page > 0:
            self.current_page -= 1
            self.stack.setCurrentIndex(self.current_page)
            self.update_progress()
            self.update_groups(self.current_page)
            self.validate_current_page(self.current_page)

    def update_progress(self) -> None:
        pct = round(((self.current_page + 1) / len(PAGES)) * 100)
        self.progress.setValue(pct)

    # ------------------------------------------------------------- VALUES --
    def get_current_values(self, index: int) -> Dict[str, str]:
        meta = self.pages[index]
        values: Dict[str, str] = {}
        for name, info in meta["inputs"].items():
            ftype = info["type"]
            if ftype == "radio":
                btn = info["group"].checkedButton()
                values[name] = btn.text() if btn else ""
            elif ftype == "select":
                values[name] = info["widget"].currentText()
            elif ftype == "text" or ftype == "number":
                values[name] = info["widget"].text()
            elif ftype == "date":
                values[name] = info["widget"].date().toString("yyyy-MM-dd")
            elif ftype == "textarea":
                values[name] = info["widget"].toPlainText()
            elif ftype == "checkbox":
                values[name] = "Yes" if info["widget"].isChecked() else "No"
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
        for field in iterate_fields(meta["spec"]["sections"][0]["fields"], values):
            name = field.get("name")
            value = values.get(name, "")
            if field.get("required"):
                if field["type"] == "checkbox":
                    if value != "Yes":
                        valid = False
                elif not value:
                    valid = False
            if valid and field.get("validate") and value:
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
        meta["next_btn"].setEnabled(valid)
        return valid

    # ------------------------------------------------------------- SIGNAL --
    def handle_field_change(self) -> None:
        self.update_groups(self.current_page)
        self.validate_current_page(self.current_page)


def main() -> None:
    app = QApplication(sys.argv)
    form = MagnusClientIntakeForm()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
