from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the welcome page"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(20)

    # Welcome message
    welcome_label = QLabel("Welcome to Magnus Client Intake Form")
    welcome_font = QFont()
    welcome_font.setPointSize(16)
    welcome_font.setBold(True)
    welcome_label.setFont(welcome_font)
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    welcome_label.setStyleSheet("color: #2c3e50; margin: 20px;")
    layout.addWidget(welcome_label)

    # Instructions
    instructions = QLabel("""
    This form will collect comprehensive information for your financial services account.

    Please ensure you have the following information ready:
    • Personal identification details
    • Employment and income information
    • Investment experience and objectives
    • Beneficiary information
    • Contact details for trusted persons

    The form includes 12 sections and takes approximately 15-20 minutes to complete.
    Your progress is automatically saved every 30 seconds.
    """)
    instructions.setWordWrap(True)
    instructions.setStyleSheet("""
        QLabel {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            font-size: 12px;
            line-height: 1.5;
        }
    """)
    layout.addWidget(instructions)

    # Navigation buttons
    layout.addLayout(form.create_navigation_buttons(back_index=None, next_index=1))

    form.stacked_widget.addWidget(widget)
