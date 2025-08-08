from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the contact information page"""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Page title
    title = QLabel("Contact Information")
    title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
    layout.addWidget(title)

    # Residential Address
    layout.addWidget(QLabel("Residential Address:"))
    address_input = QTextEdit()
    address_input.setObjectName("residential_address")
    address_input.setMaximumHeight(80)
    address_input.setPlaceholderText("Street Address\nCity, State ZIP Code")
    address_input.setStyleSheet("""
        QTextEdit {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
    """)
    layout.addWidget(address_input)

    # Email
    layout.addWidget(QLabel("Email Address:"))
    email_input = EnhancedLineEdit("email")
    email_input.setObjectName("email")
    email_input.setPlaceholderText("example@email.com")
    layout.addWidget(email_input)

    # Phone numbers
    layout.addWidget(QLabel("Home Phone:"))
    home_phone_input = EnhancedLineEdit("home_phone")
    home_phone_input.setObjectName("home_phone")
    home_phone_input.setPlaceholderText("(XXX) XXX-XXXX")
    layout.addWidget(home_phone_input)

    layout.addWidget(QLabel("Mobile Phone:"))
    mobile_phone_input = EnhancedLineEdit("mobile_phone")
    mobile_phone_input.setObjectName("mobile_phone")
    mobile_phone_input.setPlaceholderText("(XXX) XXX-XXXX")
    layout.addWidget(mobile_phone_input)

    layout.addWidget(QLabel("Work Phone:"))
    work_phone_input = EnhancedLineEdit("work_phone")
    work_phone_input.setObjectName("work_phone")
    layout.addWidget(work_phone_input)

    layout.addStretch()
    layout.addLayout(form.create_navigation_buttons(back_index=1, next_index=3))

    form.stacked_widget.addWidget(widget)
