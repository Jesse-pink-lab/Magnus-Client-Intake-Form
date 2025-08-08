from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the personal information page"""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Page title
    title = QLabel("Personal Information")
    title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
    layout.addWidget(title)

    # Form fields
    layout.addWidget(QLabel("Full Legal Name:"))
    full_name_input = EnhancedLineEdit("full_name")
    full_name_input.setObjectName("full_name")
    layout.addWidget(full_name_input)

    layout.addWidget(QLabel("Date of Birth:"))
    dob_input = QDateEdit()
    dob_input.setObjectName("dob")
    dob_input.setDate(QDate.currentDate().addYears(-30))
    dob_input.setCalendarPopup(True)
    dob_input.setStyleSheet("""
        QDateEdit {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
    """)
    layout.addWidget(dob_input)

    layout.addWidget(QLabel("Social Security Number:"))
    ssn_input = EnhancedLineEdit("ssn")
    ssn_input.setObjectName("ssn")
    ssn_input.setPlaceholderText("XXX-XX-XXXX")
    layout.addWidget(ssn_input)

    layout.addWidget(QLabel("Citizenship Status:"))
    citizenship_combo = QComboBox()
    citizenship_combo.setObjectName("citizenship")
    citizenship_combo.addItems(["", "US Citizen", "Permanent Resident", "Non-Resident Alien", "Other"])
    citizenship_combo.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
    """)
    layout.addWidget(citizenship_combo)

    layout.addWidget(QLabel("Marital Status:"))
    marital_combo = QComboBox()
    marital_combo.setObjectName("marital_status")
    marital_combo.addItems(["", "Single", "Married", "Divorced", "Widowed", "Separated"])
    marital_combo.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
    """)
    layout.addWidget(marital_combo)

    layout.addStretch()
    layout.addLayout(form.create_navigation_buttons(back_index=0, next_index=2))

    form.stacked_widget.addWidget(widget)
