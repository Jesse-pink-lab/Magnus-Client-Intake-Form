from __future__ import annotations

from typing import Any, Dict, List

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .pages import PAGES
from .state import STATE_FILE, load_state, save_state
from .renderer import PageRenderer
from .validation import VALIDATORS


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

        self.update_progress()
        self.update_groups(0)
        self.validate_current_page(0)

    # ---------------------------------------------------------- NAVIGATION --
    def on_next(self) -> None:
        if not self.validate_current_page(self.current_page):
            return
        self.state.update(self.get_current_values(self.current_page))
        save_state(STATE_FILE, self.state)
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
        save_state(STATE_FILE, self.state)
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
