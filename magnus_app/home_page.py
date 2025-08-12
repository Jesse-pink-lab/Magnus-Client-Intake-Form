from __future__ import annotations

import os
from typing import List, Dict

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)


class HomePage(QWidget):
    newRequested = pyqtSignal()
    openDialogRequested = pyqtSignal()
    openPathRequested = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        title = QLabel("Magnus Client Intake")
        title.setObjectName("homeTitle")
        layout.addWidget(title)

        header = QLabel("Home")
        header.setObjectName("homeLabel")
        layout.addWidget(header)

        btn_row = QHBoxLayout()
        new_btn = QPushButton("New Draft")
        open_btn = QPushButton("Open…")
        btn_row.addWidget(new_btn)
        btn_row.addWidget(open_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.table = QTableWidget(0, 3)
        self.table.setObjectName("recentTable")
        self.table.setHorizontalHeaderLabels(["Name", "Last Opened", "Path"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, 1)

        new_btn.clicked.connect(self.newRequested.emit)
        open_btn.clicked.connect(self.openDialogRequested.emit)
        self.table.cellDoubleClicked.connect(self._emit_open)

    # ------------------------------------------------------------------ utils --
    def refresh(self, items: List[Dict]) -> None:
        self.table.setRowCount(0)
        for item in items:
            path = item.get("path", "")
            name = os.path.basename(path)
            last_opened = item.get("last_opened", "")
            missing = not os.path.exists(path)

            row = self.table.rowCount()
            self.table.insertRow(row)

            name_text = f"{name} (missing)" if missing else name
            name_item = QTableWidgetItem(name_text)
            name_item.setData(Qt.ItemDataRole.UserRole, path)
            last_item = QTableWidgetItem(last_opened)
            path_item = QTableWidgetItem(path)

            if missing:
                for it in (name_item, last_item, path_item):
                    it.setToolTip("File not found")
                    it.setForeground(Qt.GlobalColor.gray)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, last_item)
            self.table.setItem(row, 2, path_item)

    def _emit_open(self, row: int, _: int) -> None:
        item = self.table.item(row, 0)
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.openPathRequested.emit(path)
