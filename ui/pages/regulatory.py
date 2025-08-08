from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the regulatory consent page"""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Page title
    title = QLabel("Regulatory Consent")
    title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
    layout.addWidget(title)

    # Electronic Delivery Consent
    layout.addWidget(QLabel("Electronic Delivery Consent:"))

    reg_group = QButtonGroup()

    reg_yes = QRadioButton("Yes - I consent to receive regulatory communications electronically")
    reg_yes.setObjectName("electronic_regulatory_yes")
    reg_group.addButton(reg_yes)
    layout.addWidget(reg_yes)

    reg_no = QRadioButton("No - I prefer to receive regulatory communications by mail")
    reg_no.setObjectName("electronic_regulatory_no")
    reg_group.addButton(reg_no)
    layout.addWidget(reg_no)

    # Disclosure text
    disclosure = QLabel("""
    Electronic Delivery Disclosure:

    By selecting "Yes" above, you consent to receive regulatory communications, 
    account statements, confirmations, prospectuses, and other important documents 
    electronically. You may withdraw this consent at any time by contacting us.

    Electronic delivery helps reduce paper waste and provides faster access to 
    your important documents. You will receive email notifications when new 
    documents are available in your secure online account.

    System Requirements: You must have access to a computer with internet 
    connection and email capability to receive electronic communications.
    """)
    disclosure.setWordWrap(True)
    disclosure.setStyleSheet("""
        QLabel {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-size: 11px;
            line-height: 1.4;
            border: 1px solid #dee2e6;
        }
    """)
    layout.addWidget(disclosure)

    layout.addStretch()
    layout.addLayout(form.create_navigation_buttons(back_index=9, next_index=11))

    form.stacked_widget.addWidget(widget)
