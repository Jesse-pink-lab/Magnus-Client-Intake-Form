from typing import Any, Callable, Dict, List, Tuple

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QScrollArea,
    QVBoxLayout,
    QTextEdit,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QPushButton,
)

from magnus_app.pages import ISO_COUNTRIES, PAGES


class PageRenderer:
    """Render pages and fields based on a specification."""

    def __init__(self, state: Dict[str, Any], validators: Dict[str, Callable[..., bool]]):
        self.state = state
        self.validators = validators

    # -------------------------------------------------------------- ITERATE --
    def iterate_fields(self, fields: List[Dict[str, Any]], values: Dict[str, Any]):
        """Yield field specs that should be validated based on show_if rules."""
        for fld in fields:
            ftype = fld.get("type")
            if ftype in ("group", "repeating_group"):
                # Groups (including repeating groups) may be conditionally shown
                cond = fld.get("show_if") or {}
                if cond:
                    name, val = next(iter(cond.items()))
                    if values.get(name, "") != val:
                        continue
                # For validation we simply iterate over the child field specs
                yield from self.iterate_fields(fld.get("fields", []), values)
            elif ftype != "label":
                cond = fld.get("show_if")
                if cond:
                    name, val = next(iter(cond.items()))
                    if values.get(name, "") != val:
                        continue
                yield fld

    # -------------------------------------------------------------- RENDER --
    def render_fields(
        self,
        fields: List[Dict[str, Any]],
        layout: QVBoxLayout,
        inputs: Dict[str, Dict[str, Any]],
        groups: List[Tuple[QWidget, Dict[str, str]]],
        on_change: Callable[[], None],
    ) -> None:
        for field in fields:
            ftype = field.get("type")
            name = field.get("name")
            if ftype == "group":
                container = QWidget()
                container_layout = QVBoxLayout(container)
                self.render_fields(field["fields"], container_layout, inputs, groups, on_change)
                layout.addWidget(container)
                groups.append((container, field["show_if"]))
                continue

            if ftype == "repeating_group" and name:
                container = QWidget()
                vbox = QVBoxLayout(container)
                item_inputs: List[Dict[str, Dict[str, Any]]] = []

                def add_item(data: Dict[str, Any] | None = None) -> None:
                    idx = len(item_inputs)
                    box = QGroupBox(f"{field.get('item_label', 'Item')} {idx + 1}")
                    box_layout = QVBoxLayout(box)
                    sub_inputs: Dict[str, Dict[str, Any]] = {}
                    for sub in field.get("fields", []):
                        sub_name = sub.get("name")
                        unique = f"{name}_{idx}_{sub_name}"
                        sub_spec = dict(sub)
                        sub_spec["name"] = unique
                        # Pre-fill state if data provided
                        if data:
                            self.state[unique] = data.get(sub_name, "")
                        self.render_fields([sub_spec], box_layout, sub_inputs, groups, on_change)
                        # Remember original name for later extraction
                        if unique in sub_inputs:
                            sub_inputs[unique]["orig_name"] = sub_name
                    item_inputs.append(sub_inputs)
                    vbox.addWidget(box)

                existing = self.state.get(name) or []
                if existing:
                    for item in existing:
                        add_item(item)
                else:
                    add_item()

                add_btn = QPushButton(f"Add Another {field.get('item_label', 'Item')}")
                add_btn.clicked.connect(lambda: add_item())
                vbox.addWidget(add_btn)

                layout.addWidget(container)
                inputs[name] = {
                    "type": "repeating_group",
                    "items": item_inputs,
                }
                continue

            label_text = field.get("label", name)
            widget: QWidget

            if ftype == "label":
                lab = QLabel(label_text)
                lab.setWordWrap(True)
                layout.addWidget(lab)
                continue

            if ftype == "radio":
                container = QWidget()
                hl = QHBoxLayout(container)
                lab = QLabel(label_text)
                lab.setWordWrap(True)
                hl.addWidget(lab)
                group = QButtonGroup(container)
                for opt in field.get("options", []):
                    rb = QRadioButton(opt)
                    if self.state.get(name) == opt:
                        rb.setChecked(True)
                    group.addButton(rb)
                    hl.addWidget(rb)
                    rb.toggled.connect(on_change)
                container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                inputs[name] = {"type": "radio", "group": group}
                layout.addWidget(container)
                continue

            if ftype == "select":
                widget = QComboBox()
                opts = field.get("options") or []
                if opts == "ISO_COUNTRIES":
                    opts = ISO_COUNTRIES
                widget.addItems([""] + list(opts))
                widget.setCurrentText(self.state.get(name, ""))
                widget.currentTextChanged.connect(on_change)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            elif ftype == "text":
                widget = QLineEdit()
                widget.setText(self.state.get(name, ""))
                widget.textChanged.connect(on_change)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            elif ftype == "number":
                widget = QLineEdit()
                widget.setText(self.state.get(name, ""))
                widget.textChanged.connect(on_change)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            elif ftype == "date":
                widget = QDateEdit()
                widget.setDisplayFormat("yyyy-MM-dd")
                widget.setCalendarPopup(True)
                val = self.state.get(name, "")
                if val:
                    dt = QDate.fromString(val, "yyyy-MM-dd")
                    if dt.isValid():
                        widget.setDate(dt)
                widget.dateChanged.connect(on_change)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            elif ftype == "textarea":
                widget = QTextEdit()
                widget.setPlainText(self.state.get(name, ""))
                widget.textChanged.connect(on_change)
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            elif ftype == "checkbox":
                widget = QCheckBox(label_text)
                widget.setChecked(bool(self.state.get(name, False)))
                widget.stateChanged.connect(on_change)
                label_text = ""  # label already used
            else:
                continue

            if label_text:
                lab = QLabel(label_text)
                lab.setWordWrap(True)
                layout.addWidget(lab)
            layout.addWidget(widget)
            inputs[name] = {"type": ftype, "widget": widget}

    def render_page_from_spec(
        self,
        page_spec: Dict[str, Any],
        index: int,
        on_change: Callable[[], None],
        on_next: Callable[[], None],
        on_back: Callable[[], None],
    ) -> Tuple[QWidget, Dict[str, Any]]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll, 1)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(content)

        inputs: Dict[str, Dict[str, Any]] = {}
        groups: List[Tuple[QWidget, Dict[str, str]]] = []

        for section in page_spec.get("sections", []):
            box = QGroupBox(section.get("title", ""))
            box_layout = QVBoxLayout(box)
            self.render_fields(section.get("fields", []), box_layout, inputs, groups, on_change)
            content_layout.addWidget(box)

        content_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        nav = QHBoxLayout()
        if index > 0:
            back_btn = QPushButton("Back")
            back_btn.clicked.connect(on_back)
            nav.addWidget(back_btn)
        nav.addStretch()
        if index < len(PAGES) - 1:
            next_btn = QPushButton("Next")
        else:
            next_btn = QPushButton("Finish")
        next_btn.clicked.connect(on_next)
        nav.addWidget(next_btn)
        layout.addLayout(nav)

        meta = {
            "spec": page_spec,
            "inputs": inputs,
            "groups": groups,
            "next_btn": next_btn,
        }
        return page, meta
