from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the trusted contact person page"""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Page title
    title = QLabel("Trusted Contact Person")
    title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
    layout.addWidget(title)

    # Instructions
    instructions = QLabel("""
    Please provide information for a trusted contact person. This person may be contacted 
    in the event we are unable to reach you, or if we have concerns about your health 
    or financial exploitation.
    """)
    instructions.setWordWrap(True)
    instructions.setStyleSheet("font-style: italic; color: #7f8c8d; margin-bottom: 15px;")
    layout.addWidget(instructions)

    # Trusted Contact Name
    layout.addWidget(QLabel("Full Legal Name:"))
    trusted_name_input = EnhancedLineEdit("trusted_full_name")
    trusted_name_input.setObjectName("trusted_full_name")
    layout.addWidget(trusted_name_input)

    # Trusted Contact Relationship
    layout.addWidget(QLabel("Relationship to You:"))
    trusted_relationship_input = EnhancedLineEdit("trusted_relationship")
    trusted_relationship_input.setObjectName("trusted_relationship")
    layout.addWidget(trusted_relationship_input)

    # Trusted Contact Phone
    layout.addWidget(QLabel("Phone Number:"))
    trusted_phone_input = EnhancedLineEdit("trusted_phone")
    trusted_phone_input.setObjectName("trusted_phone")
    trusted_phone_input.setPlaceholderText("(XXX) XXX-XXXX")
    layout.addWidget(trusted_phone_input)

    # Trusted Contact Email
    layout.addWidget(QLabel("Email Address:"))
    trusted_email_input = EnhancedLineEdit("trusted_email")
    trusted_email_input.setObjectName("trusted_email")
    trusted_email_input.setPlaceholderText("example@email.com")
    layout.addWidget(trusted_email_input)

    layout.addStretch()
    layout.addLayout(form.create_navigation_buttons(back_index=8, next_index=10))

    form.stacked_widget.addWidget(widget)
