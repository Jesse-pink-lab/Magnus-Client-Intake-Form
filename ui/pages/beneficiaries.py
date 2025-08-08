from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
        """Create the beneficiaries information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Page title
        title = QLabel("Beneficiaries Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Beneficiaries list container
        form.beneficiaries_layout = QVBoxLayout()
        form.beneficiaries_layout.setSpacing(10)

        form.beneficiaries_scroll_area = QScrollArea()
        form.beneficiaries_scroll_area.setWidgetResizable(True)
        form.beneficiaries_scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        beneficiaries_container = QWidget()
        beneficiaries_container.setLayout(form.beneficiaries_layout)
        form.beneficiaries_scroll_area.setWidget(beneficiaries_container)

        layout.addWidget(form.beneficiaries_scroll_area)

        # Add Beneficiary button
        add_beneficiary_btn = QPushButton("Add Beneficiary")
        add_beneficiary_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        add_beneficiary_btn.clicked.connect(form.add_beneficiary_field)
        layout.addWidget(add_beneficiary_btn)

        layout.addStretch()
        layout.addLayout(form.create_navigation_buttons(back_index=6, next_index=8))

        form.stacked_widget.addWidget(widget)
