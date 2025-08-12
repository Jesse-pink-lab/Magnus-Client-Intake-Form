from typing import Any, Callable, Dict, List, Tuple

from PyQt6.QtCore import QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
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
from .validation import (
    parse_usd,
    format_usd,
    parse_percent,
    format_percent,
    YEAR_RE,
)


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
            if ftype == "group":
                cond = fld.get("show_if") or {}
                if cond:
                    name, val = next(iter(cond.items()))
                    if values.get(name, "") != val:
                        continue
                yield from self.iterate_fields(fld.get("fields", []), values)
            elif ftype == "repeating_group":
                cond = fld.get("show_if") or {}
                if cond:
                    name, val = next(iter(cond.items()))
                    if values.get(name, "") != val:
                        continue
                name = fld.get("name")
                items = values.get(name)
                if not isinstance(items, list) or not items:
                    items = [{}]
                for i, item_vals in enumerate(items):
                    for sub in fld.get("fields", []):
                        scond = sub.get("show_if")
                        if scond:
                            sname, sval = next(iter(scond.items()))
                            if item_vals.get(sname, "") != sval:
                                continue
                        sub_spec = dict(sub)
                        sub_spec["_rg"] = {"name": name, "index": i}
                        yield sub_spec
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
            elif ftype == "repeating_group" and name:
                container = QWidget()
                vbox = QVBoxLayout(container)

                items = self.state.get(name)
                if not isinstance(items, list):
                    items = []
                    self.state[name] = items

                item_boxes: List[QGroupBox] = []

                def renumber() -> None:
                    for i, box in enumerate(item_boxes):
                        box.setTitle(f"{field.get('item_label', 'Item')} {i + 1}")

                def add_item(prefill: Dict[str, Any] | None = None) -> None:
                    idx = len(item_boxes)
                    if prefill is None:
                        prefill = {}
                    if idx >= len(items):
                        items.append(prefill)
                    box = QGroupBox(f"{field.get('item_label', 'Item')} {idx + 1}")
                    box_layout = QVBoxLayout(box)
                    for sub in field.get("fields", []):
                        self._render_repeating_subfield(name, idx, sub, box_layout, on_change)

                    remove_btn = QPushButton(f"Remove {field.get('item_label', 'Item')}")
                    remove_btn.setObjectName("btn-remove-item")

                    def do_remove() -> None:
                        pos = item_boxes.index(box)
                        items.pop(pos)
                        vbox.removeWidget(box)
                        box.deleteLater()
                        item_boxes.pop(pos)
                        renumber()
                        on_change()

                    remove_btn.clicked.connect(do_remove)
                    box_layout.addWidget(remove_btn)

                    item_boxes.append(box)
                    vbox.addWidget(box)
                    on_change()

                if items:
                    for itm in list(items):
                        add_item(itm)
                else:
                    add_item({})

                add_btn = QPushButton(f"Add Another {field.get('item_label', 'Item')}")
                add_btn.clicked.connect(lambda: add_item({}))
                vbox.addWidget(add_btn)

                layout.addWidget(container)
                if field.get("show_if"):
                    groups.append((container, field["show_if"]))
                inputs[name] = {"type": "repeating_group"}
                continue


            ftype = field.get("type")
            name = field.get("name")
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
                if field.get("input_mask") == "ssn":
                    widget.setInputMask("000-00-0000;_")
                elif field.get("input_mask") == "phone":
                    widget.setInputMask("(000) 000-0000;_")
                validator_name = field.get("validate")
                if validator_name == "usd_currency_0_1b":
                    num = parse_usd(widget.text())
                    if num is not None:
                        widget.setText(format_usd(num))
                elif validator_name == "percent_0_100":
                    num = parse_percent(widget.text())
                    if num is not None:
                        widget.setText(format_percent(num))
                widget.textChanged.connect(on_change)
                if validator_name:
                    def finish(w=widget, vname=validator_name):
                        text = w.text()
                        ok = True
                        if vname == "usd_currency_0_1b":
                            num = parse_usd(text)
                            if num is not None:
                                w.setText(format_usd(num))
                            ok = num is not None
                        elif vname == "percent_0_100":
                            num = parse_percent(text)
                            if num is not None:
                                w.setText(format_percent(num))
                            ok = num is not None
                        else:
                            validator = self.validators.get(vname)
                            if validator:
                                try:
                                    ok = validator(text, self.state)
                                except TypeError:
                                    ok = validator(text)
                        w.setStyleSheet("" if ok else "border: 1px solid #d9534f;")
                    widget.editingFinished.connect(finish)
                if field.get("validate") == "year_1900_current":
                    widget.setValidator(
                        QRegularExpressionValidator(QRegularExpression(YEAR_RE.pattern))
                    )
                if field.get("placeholder"):
                    widget.setPlaceholderText(field.get("placeholder"))
                widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            elif ftype == "number":
                widget = QLineEdit()
                widget.setText(self.state.get(name, ""))
                if field.get("input_mask") == "ssn":
                    widget.setInputMask("000-00-0000;_")
                elif field.get("input_mask") == "phone":
                    widget.setInputMask("(000) 000-0000;_")
                validator_name = field.get("validate")
                if validator_name == "usd_currency_0_1b":
                    num = parse_usd(widget.text())
                    if num is not None:
                        widget.setText(format_usd(num))
                elif validator_name == "percent_0_100":
                    num = parse_percent(widget.text())
                    if num is not None:
                        widget.setText(format_percent(num))
                widget.textChanged.connect(on_change)
                if validator_name:
                    def finish(w=widget, vname=validator_name):
                        text = w.text()
                        ok = True
                        if vname == "usd_currency_0_1b":
                            num = parse_usd(text)
                            if num is not None:
                                w.setText(format_usd(num))
                            ok = num is not None
                        elif vname == "percent_0_100":
                            num = parse_percent(text)
                            if num is not None:
                                w.setText(format_percent(num))
                            ok = num is not None
                        else:
                            validator = self.validators.get(vname)
                            if validator:
                                try:
                                    ok = validator(text, self.state)
                                except TypeError:
                                    ok = validator(text)
                        w.setStyleSheet("" if ok else "border: 1px solid #d9534f;")
                    widget.editingFinished.connect(finish)
                if field.get("validate") == "year_1900_current":
                    widget.setValidator(
                        QRegularExpressionValidator(QRegularExpression(YEAR_RE.pattern))
                    )
                if field.get("placeholder"):
                    widget.setPlaceholderText(field.get("placeholder"))
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
                if field.get("validate") in ("date_adult", "date_optional"):
                    widget.setMinimumDate(QDate(1900, 1, 1))
                    widget.setMaximumDate(QDate.currentDate())
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

    def _render_repeating_subfield(
        self,
        group_name: str,
        index: int,
        sub_spec: Dict[str, Any],
        layout: QVBoxLayout,
        on_change: Callable[[], None],
    ) -> None:
        sub_name = sub_spec.get("name")
        ftype = sub_spec.get("type")
        label_text = sub_spec.get("label", sub_name)
        data = self.state[group_name][index]

        def set_value(val: Any) -> None:
            data[sub_name] = val
            on_change()

        if ftype == "radio":
            container = QWidget()
            hl = QHBoxLayout(container)
            lab = QLabel(label_text)
            lab.setWordWrap(True)
            hl.addWidget(lab)
            group = QButtonGroup(container)
            for opt in sub_spec.get("options", []):
                rb = QRadioButton(opt)
                if data.get(sub_name) == opt:
                    rb.setChecked(True)
                group.addButton(rb)
                hl.addWidget(rb)
                rb.toggled.connect(lambda checked, opt=opt: set_value(opt) if checked else None)
            container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            layout.addWidget(container)
            return

        if ftype == "select":
            widget = QComboBox()
            opts = sub_spec.get("options") or []
            if opts == "ISO_COUNTRIES":
                opts = ISO_COUNTRIES
            widget.addItems([""] + list(opts))
            widget.setCurrentText(data.get(sub_name, ""))
            widget.currentTextChanged.connect(lambda val: set_value(val))
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        elif ftype == "text":
            widget = QLineEdit()
            widget.setText(data.get(sub_name, ""))
            if sub_spec.get("input_mask") == "ssn":
                widget.setInputMask("000-00-0000;_")
            elif sub_spec.get("input_mask") == "phone":
                widget.setInputMask("(000) 000-0000;_")
            validator_name = sub_spec.get("validate")
            if validator_name == "usd_currency_0_1b":
                num = parse_usd(widget.text())
                if num is not None:
                    widget.setText(format_usd(num))
            elif validator_name == "percent_0_100":
                num = parse_percent(widget.text())
                if num is not None:
                    widget.setText(format_percent(num))
            widget.textChanged.connect(lambda val: set_value(val))
            if validator_name:
                def finish(w=widget, vname=validator_name):
                    text = w.text()
                    ok = True
                    if vname == "usd_currency_0_1b":
                        num = parse_usd(text)
                        if num is not None:
                            w.setText(format_usd(num))
                        ok = num is not None
                    elif vname == "percent_0_100":
                        num = parse_percent(text)
                        if num is not None:
                            w.setText(format_percent(num))
                        ok = num is not None
                    else:
                        validator = self.validators.get(vname)
                        if validator:
                            try:
                                ok = validator(text, self.state)
                            except TypeError:
                                ok = validator(text)
                    w.setStyleSheet("" if ok else "border: 1px solid #d9534f;")
                widget.editingFinished.connect(finish)
            if sub_spec.get("validate") == "year_1900_current":
                widget.setValidator(
                    QRegularExpressionValidator(QRegularExpression(YEAR_RE.pattern))
                )
            if sub_spec.get("placeholder"):
                widget.setPlaceholderText(sub_spec.get("placeholder"))
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        elif ftype == "number":
            widget = QLineEdit()
            widget.setText(data.get(sub_name, ""))
            if sub_spec.get("input_mask") == "ssn":
                widget.setInputMask("000-00-0000;_")
            elif sub_spec.get("input_mask") == "phone":
                widget.setInputMask("(000) 000-0000;_")
            validator_name = sub_spec.get("validate")
            if validator_name == "usd_currency_0_1b":
                num = parse_usd(widget.text())
                if num is not None:
                    widget.setText(format_usd(num))
            elif validator_name == "percent_0_100":
                num = parse_percent(widget.text())
                if num is not None:
                    widget.setText(format_percent(num))
            widget.textChanged.connect(lambda val: set_value(val))
            if validator_name:
                def finish(w=widget, vname=validator_name):
                    text = w.text()
                    ok = True
                    if vname == "usd_currency_0_1b":
                        num = parse_usd(text)
                        if num is not None:
                            w.setText(format_usd(num))
                        ok = num is not None
                    elif vname == "percent_0_100":
                        num = parse_percent(text)
                        if num is not None:
                            w.setText(format_percent(num))
                        ok = num is not None
                    else:
                        validator = self.validators.get(vname)
                        if validator:
                            try:
                                ok = validator(text, self.state)
                            except TypeError:
                                ok = validator(text)
                    w.setStyleSheet("" if ok else "border: 1px solid #d9534f;")
                widget.editingFinished.connect(finish)
            if sub_spec.get("validate") == "year_1900_current":
                widget.setValidator(
                    QRegularExpressionValidator(QRegularExpression(YEAR_RE.pattern))
                )
            if sub_spec.get("placeholder"):
                widget.setPlaceholderText(sub_spec.get("placeholder"))
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        elif ftype == "date":
            widget = QDateEdit()
            widget.setDisplayFormat("yyyy-MM-dd")
            widget.setCalendarPopup(True)
            val = data.get(sub_name, "")
            if val:
                dt = QDate.fromString(val, "yyyy-MM-dd")
                if dt.isValid():
                    widget.setDate(dt)
            if sub_spec.get("validate") in ("date_adult", "date_optional"):
                widget.setMinimumDate(QDate(1900, 1, 1))
                widget.setMaximumDate(QDate.currentDate())
            widget.dateChanged.connect(lambda dt: set_value(dt.toString("yyyy-MM-dd")))
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        elif ftype == "textarea":
            widget = QTextEdit()
            widget.setPlainText(data.get(sub_name, ""))
            widget.textChanged.connect(lambda: set_value(widget.toPlainText()))
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        elif ftype == "checkbox":
            widget = QCheckBox(label_text)
            widget.setChecked(bool(data.get(sub_name, False)))
            widget.stateChanged.connect(lambda state: set_value(bool(state)))
            label_text = ""
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        else:
            return

        if label_text:
            lab = QLabel(label_text)
            lab.setWordWrap(True)
            layout.addWidget(lab)
        layout.addWidget(widget)

    def render_page_from_spec(
        self,
        page_spec: Dict[str, Any],
        index: int,
        on_change: Callable[[], None],
        on_next: Callable[[], None],
        on_back: Callable[[], None],
        on_home: Callable[[], None],
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
        home_btn = QPushButton("Home")
        home_btn.clicked.connect(on_home)
        nav.addWidget(home_btn)

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
