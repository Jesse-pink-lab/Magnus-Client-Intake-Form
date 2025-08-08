from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
        """Create the spouse information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Page title
        title = QLabel("Spouse/Partner Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Checkbox for spouse applicability
        spouse_applicable_checkbox = QCheckBox("N/A (I do not have a spouse/partner)")
        spouse_applicable_checkbox.setObjectName("spouse_applicable")
        spouse_applicable_checkbox.stateChanged.connect(form.on_spouse_applicable_changed)
        layout.addWidget(spouse_applicable_checkbox)

        # Spouse Name
        layout.addWidget(QLabel("Full Legal Name:"))
        spouse_name_input = EnhancedLineEdit("spouse_full_name")
        spouse_name_input.setObjectName("spouse_full_name")
        layout.addWidget(spouse_name_input)

        # Spouse Date of Birth
        layout.addWidget(QLabel("Date of Birth:"))
        spouse_dob_input = QDateEdit()
        spouse_dob_input.setObjectName("spouse_dob")
        spouse_dob_input.setDate(QDate.currentDate().addYears(-30))
        spouse_dob_input.setCalendarPopup(True)
        spouse_dob_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(spouse_dob_input)

        # Spouse SSN
        layout.addWidget(QLabel("Social Security Number:"))
        spouse_ssn_input = EnhancedLineEdit("spouse_ssn")
        spouse_ssn_input.setObjectName("spouse_ssn")
        spouse_ssn_input.setPlaceholderText("XXX-XX-XXXX")
        layout.addWidget(spouse_ssn_input)

        # Spouse Employment Status
        layout.addWidget(QLabel("Employment Status:"))
        spouse_employment_combo = QComboBox()
        spouse_employment_combo.setObjectName("spouse_employment_status")
        spouse_employment_combo.addItems([
            "", "Employed", "Self-Employed", "Unemployed", "Retired", 
            "Student", "Homemaker", "Disabled"
        ])
        spouse_employment_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(spouse_employment_combo)

        # Spouse Employer Information
        layout.addWidget(QLabel("Employer Name:"))
        spouse_employer_input = EnhancedLineEdit("spouse_employer_name")
        spouse_employer_input.setObjectName("spouse_employer_name")
        layout.addWidget(spouse_employer_input)

        layout.addWidget(QLabel("Occupation/Job Title:"))
        spouse_occupation_input = EnhancedLineEdit("spouse_occupation")
        spouse_occupation_input.setObjectName("spouse_occupation")
        layout.addWidget(spouse_occupation_input)

        layout.addStretch()
        layout.addLayout(form.create_navigation_buttons(back_index=4, next_index=6))

        form.stacked_widget.addWidget(widget)
