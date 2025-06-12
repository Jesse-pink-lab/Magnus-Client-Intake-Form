#!/usr/bin/env python3
"""
Magnus Client Intake Form - Enhanced Version 2.2
Professional client intake form for financial services with comprehensive validation,
security features, and PDF generation capabilities.
"""

import sys
import os
import json
import tempfile
from datetime import datetime
from typing import Dict, Any, List

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QStackedWidget, QFrame, 
    ComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton,
    QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox,
    QProgressBar, QFileDialog, 
)
import traceback
from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon

# Import custom modules
from validation import form_validator
from security import DataSecurity
from pdf_generator_reportlab import generate_pdf_from_data


class EnhancedLineEdit(QLineEdit):
    """Enhanced QLineEdit with validation feedback"""
    
    def __init__(self, field_name: str, parent=None):
        super().__init__(parent)
        self.field_name = field_name
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
    def validate_field(self) -> bool:
        """Validate field content and update styling"""
        text = self.text().strip()
        
        # Basic validation based on field name
        if "email" in self.field_name.lower():
            valid = form_validator.validate_email(self.field_name, text)
        elif "ssn" in self.field_name.lower():
            valid = form_validator.validate_ssn(self.field_name, text)
        elif "phone" in self.field_name.lower():
            valid = form_validator.validate_phone(self.field_name, text)
        else:
            valid = len(text) > 0 if text else True
        
        # Update styling based on validation
        if text and not valid:
            self.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #f44336;
                    border-radius: 4px;
                    font-size: 12px;
                    background-color: #ffebee;
                }
            """)
        elif text and valid:
            self.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #4CAF50;
                    border-radius: 4px;
                    font-size: 12px;
                    background-color: #e8f5e8;
                }
            """)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #ddd;
                    border-radius: 4px;
                    font-size: 12px;
                }
            """)
        
        return valid


class MagnusClientIntakeForm(QMainWindow):
    """Main application window for Magnus Client Intake Form"""
    
    def __init__(self):
        super().__init__()
        self.security_manager = DataSecurity()
        self.form_data = {}
        self.current_page = 0
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_data)
        self.auto_save_timer.start(30000)  # Auto-save every 30 seconds
        
        self.init_ui()
        self.load_draft_data()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Magnus Client Intake Form v2.2")
        self.setGeometry(100, 100, 900, 700)
        
        # Set application icon
        if os.path.exists("ICON.ico"):
            self.setWindowIcon(QIcon("ICON.ico"))
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Magnus Client Intake Form")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        header_layout.addWidget(title_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(12)
        self.progress_bar.setValue(1)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        header_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(header_layout)
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create all pages
        self.create_welcome_page()           # Page 0
        self.create_personal_info_page()     # Page 1
        self.create_contact_info_page()      # Page 2
        self.create_employment_info_page()   # Page 3
        self.create_financial_info_page()    # Page 4
        self.create_spouse_info_page()       # Page 5
        self.create_dependents_page()        # Page 6
        self.create_beneficiaries_page()     # Page 7
        self.create_assets_investment_page() # Page 8
        self.create_trusted_contact_page()   # Page 9
        self.create_regulatory_page()        # Page 10
        self.create_review_submit_page()     # Page 11
        
        # Status bar
        self.statusBar().showMessage("Ready - Page 1 of 12")
        
    def create_welcome_page(self):
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
        layout.addLayout(self.create_navigation_buttons(back_index=None, next_index=1))
        
        self.stacked_widget.addWidget(widget)
        
    def create_personal_info_page(self):
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
        layout.addLayout(self.create_navigation_buttons(back_index=0, next_index=2))
        
        self.stacked_widget.addWidget(widget)
        
    def create_contact_info_page(self):
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
        layout.addLayout(self.create_navigation_buttons(back_index=1, next_index=3))
        
        self.stacked_widget.addWidget(widget)
        
    def create_employment_info_page(self):
        """Create the employment information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Page title
        title = QLabel("Employment Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Employment Status
        layout.addWidget(QLabel("Employment Status:"))
        employment_combo = QComboBox()
        employment_combo.setObjectName("employment_status")
        employment_combo.addItems([
            "", "Employed", "Self-Employed", "Unemployed", "Retired", 
            "Student", "Homemaker", "Disabled"
        ])
        employment_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        employment_combo.currentTextChanged.connect(self.on_employment_status_changed)
        layout.addWidget(employment_combo)
        
        # Employer Information
        layout.addWidget(QLabel("Employer Name:"))
        employer_input = EnhancedLineEdit("employer_name")
        employer_input.setObjectName("employer_name")
        layout.addWidget(employer_input)
        
        layout.addWidget(QLabel("Occupation/Job Title:"))
        occupation_input = EnhancedLineEdit("occupation")
        occupation_input.setObjectName("occupation")
        layout.addWidget(occupation_input)
        
        layout.addWidget(QLabel("Years with Current Employer:"))
        years_employed_input = QSpinBox()
        years_employed_input.setObjectName("years_employed")
        years_employed_input.setRange(0, 50)
        years_employed_input.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(years_employed_input)
        
        # Annual Income
        layout.addWidget(QLabel("Annual Income:"))
        annual_income_input = EnhancedLineEdit("annual_income")
        annual_income_input.setObjectName("annual_income")
        annual_income_input.setPlaceholderText("Enter annual income in USD")
        layout.addWidget(annual_income_input)
        
        # Retirement-specific fields (initially hidden)
        self.retirement_group = QGroupBox("Retirement Information")
        self.retirement_group.setObjectName("retirement_group")
        self.retirement_group.setVisible(False)
        retirement_layout = QVBoxLayout(self.retirement_group)
        
        retirement_layout.addWidget(QLabel("Former Employer:"))
        former_employer_input = EnhancedLineEdit("former_employer")
        former_employer_input.setObjectName("former_employer")
        retirement_layout.addWidget(former_employer_input)
        
        retirement_layout.addWidget(QLabel("Source of Income:"))
        income_source_input = EnhancedLineEdit("income_source")
        income_source_input.setObjectName("income_source")
        retirement_layout.addWidget(income_source_input)
        
        layout.addWidget(self.retirement_group)
        
        layout.addStretch()
        layout.addLayout(self.create_navigation_buttons(back_index=2, next_index=4))
        
        self.stacked_widget.addWidget(widget)
        
    def on_employment_status_changed(self, text):
        """Handle employment status change to show/hide retirement fields"""
        if text == "Retired":
            self.retirement_group.setVisible(True)
        else:
            self.retirement_group.setVisible(False)
            
    def create_financial_info_page(self):
        """Create the financial information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Page title
        title = QLabel("Financial Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Education Status
        layout.addWidget(QLabel("Education Status:"))
        education_combo = QComboBox()
        education_combo.setObjectName("education_status")
        education_combo.addItems([
            "", "High School", "Some College", "Associate Degree", 
            "Bachelor's Degree", "Master's Degree", "Doctorate", "Other"
        ])
        education_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(education_combo)
        
        # Tax Bracket
        layout.addWidget(QLabel("Estimated Tax Bracket (%):"))
        tax_bracket_spin = QSpinBox()
        tax_bracket_spin.setObjectName("tax_bracket")
        tax_bracket_spin.setRange(0, 100)
        tax_bracket_spin.setSuffix("%")
        tax_bracket_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(tax_bracket_spin)
        
        # Risk Tolerance
        layout.addWidget(QLabel("Investment Risk Tolerance:"))
        risk_combo = QComboBox()
        risk_combo.setObjectName("risk_tolerance")
        risk_combo.addItems(["", "Conservative", "Moderate", "Aggressive"])
        risk_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(risk_combo)
        
        # Investment Objectives
        layout.addWidget(QLabel("Primary Investment Objectives:"))
        objectives_text = QTextEdit()
        objectives_text.setObjectName("investment_objectives")
        objectives_text.setMaximumHeight(80)
        objectives_text.setPlaceholderText("e.g., Retirement, Wealth Growth, Education Savings")
        objectives_text.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        layout.addWidget(objectives_text)
        
        # Net Worth
        layout.addWidget(QLabel("Estimated Net Worth (excluding primary residence):"))
        net_worth_input = EnhancedLineEdit("net_worth")
        net_worth_input.setObjectName("net_worth")
        net_worth_input.setPlaceholderText("Enter estimated net worth in USD")
        layout.addWidget(net_worth_input)
        
        # Liquid Net Worth
        layout.addWidget(QLabel("Estimated Liquid Net Worth (cash + marketable securities):"))
        liquid_net_worth_input = EnhancedLineEdit("liquid_net_worth")
        liquid_net_worth_input.setObjectName("liquid_net_worth")
        liquid_net_worth_input.setPlaceholderText("Enter estimated liquid net worth in USD")
        layout.addWidget(liquid_net_worth_input)
        
        layout.addStretch()
        layout.addLayout(self.create_navigation_buttons(back_index=3, next_index=5))
        
        self.stacked_widget.addWidget(widget)
        
    def create_spouse_info_page(self):
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
        spouse_applicable_checkbox.stateChanged.connect(self.on_spouse_applicable_changed)
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
        layout.addLayout(self.create_navigation_buttons(back_index=4, next_index=6))
        
        self.stacked_widget.addWidget(widget)
        
    def on_spouse_applicable_changed(self, state):
        """Handle spouse applicable checkbox change"""
        is_checked = state == Qt.CheckState.Checked.value
        
        # Disable/enable spouse-related fields
        for widget_name in [
            "spouse_full_name", "spouse_dob", "spouse_ssn", 
            "spouse_employment_status", "spouse_employer_name", "spouse_occupation"
        ]:
            widget = self.findChild(QWidget, widget_name)
            if widget:
                widget.setEnabled(not is_checked)
                
    def create_dependents_page(self):
        """Create the dependents information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Page title
        title = QLabel("Dependents Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Dependents list container
        self.dependents_layout = QVBoxLayout()
        self.dependents_layout.setSpacing(10)
        
        self.dependents_scroll_area = QScrollArea()
        self.dependents_scroll_area.setWidgetResizable(True)
        self.dependents_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        dependents_container = QWidget()
        dependents_container.setLayout(self.dependents_layout)
        self.dependents_scroll_area.setWidget(dependents_container)
        
        layout.addWidget(self.dependents_scroll_area)
        
        # Add Dependent button
        add_dependent_btn = QPushButton("Add Dependent")
        add_dependent_btn.setStyleSheet("""
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
        add_dependent_btn.clicked.connect(self.add_dependent_field)
        layout.addWidget(add_dependent_btn)
        
        layout.addStretch()
        layout.addLayout(self.create_navigation_buttons(back_index=5, next_index=7))
        
        self.stacked_widget.addWidget(widget)
        
    def add_dependent_field(self, dependent_data=None):
        """Add fields for a new dependent"""
        dependent_frame = QFrame()
        dependent_frame.setFrameShape(QFrame.Shape.StyledPanel)
        dependent_frame.setFrameShadow(QFrame.Shadow.Raised)
        dependent_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        
        frame_layout = QVBoxLayout(dependent_frame)
        
        # Name
        frame_layout.addWidget(QLabel("Dependent Full Name:"))
        name_input = EnhancedLineEdit("dependent_name")
        name_input.setObjectName(f"dependent_name_{self.dependents_layout.count()}")
        frame_layout.addWidget(name_input)
        
        # Date of Birth
        frame_layout.addWidget(QLabel("Dependent Date of Birth:"))
        dob_input = QDateEdit()
        dob_input.setObjectName(f"dependent_dob_{self.dependents_layout.count()}")
        dob_input.setDate(QDate.currentDate().addYears(-10))
        dob_input.setCalendarPopup(True)
        dob_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        frame_layout.addWidget(dob_input)
        
        # Relationship
        frame_layout.addWidget(QLabel("Relationship:"))
        relationship_input = EnhancedLineEdit("dependent_relationship")
        relationship_input.setObjectName(f"dependent_relationship_{self.dependents_layout.count()}")
        frame_layout.addWidget(relationship_input)
        
        # Remove button
        remove_btn = QPushButton("Remove Dependent")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_dependent_field(dependent_frame))
        frame_layout.addWidget(remove_btn)
        
        self.dependents_layout.addWidget(dependent_frame)
        
        if dependent_data:
            name_input.setText(dependent_data.get("name", ""))
            dob_input.setDate(QDate.fromString(dependent_data.get("dob", ""), "MM/dd/yyyy"))
            relationship_input.setText(dependent_data.get("relationship", ""))
            
    def remove_dependent_field(self, frame):
        """Remove dependent fields"""
        frame.deleteLater()
        
    def create_beneficiaries_page(self):
        """Create the beneficiaries information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Page title
        title = QLabel("Beneficiaries Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Beneficiaries list container
        self.beneficiaries_layout = QVBoxLayout()
        self.beneficiaries_layout.setSpacing(10)
        
        self.beneficiaries_scroll_area = QScrollArea()
        self.beneficiaries_scroll_area.setWidgetResizable(True)
        self.beneficiaries_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        beneficiaries_container = QWidget()
        beneficiaries_container.setLayout(self.beneficiaries_layout)
        self.beneficiaries_scroll_area.setWidget(beneficiaries_container)
        
        layout.addWidget(self.beneficiaries_scroll_area)
        
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
        add_beneficiary_btn.clicked.connect(self.add_beneficiary_field)
        layout.addWidget(add_beneficiary_btn)
        
        layout.addStretch()
        layout.addLayout(self.create_navigation_buttons(back_index=6, next_index=8))
        
        self.stacked_widget.addWidget(widget)
        
    def add_beneficiary_field(self, beneficiary_data=None):
        """Add fields for a new beneficiary"""
        beneficiary_frame = QFrame()
        beneficiary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        beneficiary_frame.setFrameShadow(QFrame.Shadow.Raised)
        beneficiary_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #f0f0f0;
            }
        """)
        
        frame_layout = QVBoxLayout(beneficiary_frame)
        
        # Name
        frame_layout.addWidget(QLabel("Beneficiary Full Name:"))
        name_input = EnhancedLineEdit("beneficiary_name")
        name_input.setObjectName(f"beneficiary_name_{self.beneficiaries_layout.count()}")
        frame_layout.addWidget(name_input)
        
        # Date of Birth
        frame_layout.addWidget(QLabel("Beneficiary Date of Birth:"))
        dob_input = QDateEdit()
        dob_input.setObjectName(f"beneficiary_dob_{self.beneficiaries_layout.count()}")
        dob_input.setDate(QDate.currentDate().addYears(-10))
        dob_input.setCalendarPopup(True)
        dob_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        frame_layout.addWidget(dob_input)
        
        # Relationship
        frame_layout.addWidget(QLabel("Relationship:"))
        relationship_input = EnhancedLineEdit("beneficiary_relationship")
        relationship_input.setObjectName(f"beneficiary_relationship_{self.beneficiaries_layout.count()}")
        frame_layout.addWidget(relationship_input)
        
        # Percentage
        frame_layout.addWidget(QLabel("Allocation Percentage (%):"))
        percentage_spin = QSpinBox()
        percentage_spin.setObjectName(f"beneficiary_percentage_{self.beneficiaries_layout.count()}")
        percentage_spin.setRange(0, 100)
        percentage_spin.setSuffix("%")
        percentage_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        frame_layout.addWidget(percentage_spin)
        
        # Remove button
        remove_btn = QPushButton("Remove Beneficiary")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_beneficiary_field(beneficiary_frame))
        frame_layout.addWidget(remove_btn)
        
        self.beneficiaries_layout.addWidget(beneficiary_frame)
        
        if beneficiary_data:
            name_input.setText(beneficiary_data.get("name", ""))
            dob_input.setDate(QDate.fromString(beneficiary_data.get("dob", ""), "MM/dd/yyyy"))
            relationship_input.setText(beneficiary_data.get("relationship", ""))
            percentage_spin.setValue(beneficiary_data.get("percentage", 0))
            
    def remove_beneficiary_field(self, frame):
        """Remove beneficiary fields"""
        frame.deleteLater()
        
    def create_assets_investment_page(self):
        """Create the assets and investment experience page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Page title
        title = QLabel("Assets & Investment Experience")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Net Worth
        layout.addWidget(QLabel("Estimated Net Worth (excluding primary residence):"))
        net_worth_input = EnhancedLineEdit("net_worth")
        net_worth_input.setObjectName("net_worth")
        net_worth_input.setPlaceholderText("Enter estimated net worth in USD")
        layout.addWidget(net_worth_input)
        
        # Liquid Net Worth
        layout.addWidget(QLabel("Estimated Liquid Net Worth (cash + marketable securities):"))
        liquid_net_worth_input = EnhancedLineEdit("liquid_net_worth")
        liquid_net_worth_input.setObjectName("liquid_net_worth")
        liquid_net_worth_input.setPlaceholderText("Enter estimated liquid net worth in USD")
        layout.addWidget(liquid_net_worth_input)
        
        # Assets Held Away
        layout.addWidget(QLabel("Assets Held Away (e.g., Brokerage Accounts, 401k, etc.):"))
        assets_held_away_input = EnhancedLineEdit("assets_held_away")
        assets_held_away_input.setObjectName("assets_held_away")
        assets_held_away_input.setPlaceholderText("Enter total value of assets held away in USD")
        layout.addWidget(assets_held_away_input)
        
        # Asset Breakdown (optional)
        include_breakdown_checkbox = QCheckBox("Include Asset Breakdown")
        include_breakdown_checkbox.setObjectName("include_breakdown")
        include_breakdown_checkbox.stateChanged.connect(self.on_include_breakdown_changed)
        layout.addWidget(include_breakdown_checkbox)
        
        self.asset_breakdown_group = QGroupBox("Asset Breakdown")
        self.asset_breakdown_group.setObjectName("asset_breakdown_group")
        self.asset_breakdown_group.setVisible(False)
        
        breakdown_layout = QVBoxLayout(self.asset_breakdown_group)
        self.asset_breakdown_fields = {}
        
        asset_types = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Options", "Futures", "Short-Term", "Other"]
        for asset_type in asset_types:
            h_layout = QHBoxLayout()
            label = QLabel(f"{asset_type} (%):")
            spin_box = QSpinBox()
            spin_box.setObjectName(f"asset_breakdown_{asset_type.lower().replace(' ', '_')}")
            self.asset_breakdown_fields[asset_type] = spin_box
            
            h_layout.addWidget(label)
            h_layout.addWidget(spin_box)
            breakdown_layout.addLayout(h_layout)
            
        layout.addWidget(self.asset_breakdown_group)
        
        # Investment Experience by Asset Type
        layout.addWidget(QLabel("Investment Experience by Asset Type:"))
        
        self.asset_experience_layout = QVBoxLayout()
        self.asset_experience_fields = {}
        
        experience_types = ["Stocks", "Bonds", "Mutual Funds", "ETFs", "Options", "Futures"]
        for exp_type in experience_types:
            group_box = QGroupBox(exp_type)
            group_box_layout = QHBoxLayout(group_box)
            
            year_label = QLabel("Year Started:")
            year_input = QLineEdit()
            year_input.setObjectName(f"asset_experience_{exp_type.lower().replace(' ', '_')}_year")
            year_input.setPlaceholderText("YYYY")
            year_input.setMaximumWidth(80)
            
            level_label = QLabel("Level:")
            level_combo = QComboBox()
            level_combo.setObjectName(f"asset_experience_{exp_type.lower().replace(' ', '_')}_level")
            level_combo.addItems(["", "None", "Limited", "Good", "Extensive"])
            
            group_box_layout.addWidget(year_label)
            group_box_layout.addWidget(year_input)
            group_box_layout.addWidget(level_label)
            group_box_layout.addWidget(level_combo)
            
            self.asset_experience_fields[exp_type] = {"year": year_input, "level": level_combo}
            self.asset_experience_layout.addWidget(group_box)
            
        layout.addLayout(self.asset_experience_layout)
        
        # Outside Broker Firm
        has_outside_broker_checkbox = QCheckBox("Do you have assets with an outside broker firm?")
        has_outside_broker_checkbox.setObjectName("has_outside_broker")
        has_outside_broker_checkbox.stateChanged.connect(self.on_has_outside_broker_changed)
        layout.addWidget(has_outside_broker_checkbox)
        
        self.outside_broker_group = QGroupBox("Outside Broker Firm Information")
        self.outside_broker_group.setObjectName("outside_broker_group")
        self.outside_broker_group.setVisible(False)
        
        outside_broker_layout = QVBoxLayout(self.outside_broker_group)
        
        outside_broker_layout.addWidget(QLabel("Firm Name:"))
        outside_firm_name_input = EnhancedLineEdit("outside_firm_name")
        outside_firm_name_input.setObjectName("outside_firm_name")
        outside_broker_layout.addWidget(outside_firm_name_input)
        
        outside_broker_layout.addWidget(QLabel("Liquid Amount with this Firm:"))
        outside_liquid_amount_input = EnhancedLineEdit("outside_liquid_amount")
        outside_liquid_amount_input.setObjectName("outside_liquid_amount")
        outside_liquid_amount_input.setPlaceholderText("Enter liquid amount in USD")
        outside_broker_layout.addWidget(outside_liquid_amount_input)
        
        layout.addWidget(self.outside_broker_group)
        
        layout.addStretch()
        layout.addLayout(self.create_navigation_buttons(back_index=7, next_index=9))
        
        self.stacked_widget.addWidget(widget)
        
    def on_include_breakdown_changed(self, state):
        """Handle include breakdown checkbox change"""
        is_checked = state == Qt.CheckState.Checked.value
        self.asset_breakdown_group.setVisible(is_checked)
        
    def on_has_outside_broker_changed(self, state):
        """Handle has outside broker checkbox change"""
        is_checked = state == Qt.CheckState.Checked.value
        self.outside_broker_group.setVisible(is_checked)
        
    def create_trusted_contact_page(self):
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
        layout.addLayout(self.create_navigation_buttons(back_index=8, next_index=10))
        
        self.stacked_widget.addWidget(widget)
        
    def create_regulatory_page(self):
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
        layout.addLayout(self.create_navigation_buttons(back_index=9, next_index=11))
        
        self.stacked_widget.addWidget(widget)
        
    def create_review_submit_page(self):
        """Create the review and submit page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Page title
        title = QLabel("Review & Submit")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Please review your information and submit the form to generate your PDF report.")
        instructions.setStyleSheet("font-style: italic; color: #7f8c8d; margin-bottom: 15px;")
        layout.addWidget(instructions)
        
        # Review area
        self.review_area = QTextEdit()
        self.review_area.setReadOnly(True)
        self.review_area.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-family: monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.review_area)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        save_draft_btn = QPushButton("Save Draft")
        save_draft_btn.clicked.connect(self.save_draft)
        save_draft_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        button_layout.addWidget(save_draft_btn)
        
        generate_pdf_btn = QPushButton("Generate PDF Report")
        generate_pdf_btn.clicked.connect(self.generate_pdf_report)
        generate_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        button_layout.addWidget(generate_pdf_btn)
        
        layout.addLayout(button_layout)
        layout.addLayout(self.create_navigation_buttons(back_index=10, next_index=None))
        
        self.stacked_widget.addWidget(widget)
        
    def create_navigation_buttons(self, back_index=None, next_index=None):
        """Create navigation buttons layout"""
        layout = QHBoxLayout()
        
        if back_index is not None:
            back_btn = QPushButton("← Back")
            back_btn.clicked.connect(lambda: self.navigate_to_page(back_index))
            back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
            layout.addWidget(back_btn)
        
        layout.addStretch()
        
        if next_index is not None:
            next_btn = QPushButton("Next →")
            next_btn.clicked.connect(lambda: self.navigate_to_page(next_index))
            next_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            layout.addWidget(next_btn)
        
        return layout
        
    def navigate_to_page(self, page_index):
        """Navigate to a specific page"""
        if page_index == 11:  # Review page
            self.update_review_area()
        
        self.current_page = page_index
        self.stacked_widget.setCurrentIndex(page_index)
        self.progress_bar.setValue(page_index + 1)
        self.statusBar().showMessage(f"Page {page_index + 1} of 12")
        
        # Auto-save when navigating
        self.collect_form_data()
        
    def update_review_area(self):
        """Update the review area with current form data"""
        self.collect_form_data()
        
        review_text = "=== MAGNUS CLIENT INTAKE FORM - REVIEW ===\n\n"
        
        sections = [
            ("PERSONAL INFORMATION", ["full_name", "dob", "ssn", "citizenship", "marital_status"]),
            ("CONTACT INFORMATION", ["residential_address", "email", "home_phone", "mobile_phone", "work_phone"]),
            ("EMPLOYMENT INFORMATION", ["employment_status", "employer_name", "occupation", "years_employed", "annual_income"]),
            ("FINANCIAL INFORMATION", ["education_status", "tax_bracket", "risk_tolerance", "investment_objectives", "net_worth", "liquid_net_worth"]),
            ("SPOUSE INFORMATION", ["spouse_name", "spouse_dob", "spouse_ssn", "spouse_employment"]),
            ("DEPENDENTS", ["dependents"]),
            ("BENEFICIARIES", ["primary_beneficiaries", "contingent_beneficiaries"]),
        ]
        
        for section_name, fields in sections:
            review_text += f"{section_name}:\n"
            for field in fields:
                value = self.form_data.get(field, "")
                if value:
                    field_label = field.replace("_", " ").title()
                    review_text += f"  {field_label}: {value}\n"
            review_text += "\n"
        
        self.review_area.setPlainText(review_text)
        
    def collect_form_data(self):
        """Collect all form data from the UI"""
        # Get all widgets with object names
        for widget in self.findChildren((QLineEdit, QComboBox, QDateEdit, QTextEdit, QSpinBox, QCheckBox, QRadioButton)):
            object_name = widget.objectName()
            if object_name:
                if isinstance(widget, QLineEdit):
                    self.form_data[object_name] = widget.text()
                elif isinstance(widget, QComboBox):
                    self.form_data[object_name] = widget.currentText()
                elif isinstance(widget, QDateEdit):
                    self.form_data[object_name] = widget.date().toString("MM/dd/yyyy")
                elif isinstance(widget, QTextEdit):
                    self.form_data[object_name] = widget.toPlainText()
                elif isinstance(widget, QSpinBox):
                    self.form_data[object_name] = widget.value()
                elif isinstance(widget, QCheckBox):
                    self.form_data[object_name] = widget.isChecked()
                elif isinstance(widget, QRadioButton):
                    if widget.isChecked():
                        self.form_data[object_name] = True
                        
    def auto_save_data(self):
        """Auto-save form data"""
        self.collect_form_data()
        try:
            # Save to temporary file
            temp_file = os.path.join(tempfile.gettempdir(), "magnus_form_autosave.json")
            with open(temp_file, 'w') as f:
                json.dump(self.form_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Auto-save failed: {e}")
            
    def load_draft_data(self):
        """Load draft data if available"""
        try:
            temp_file = os.path.join(tempfile.gettempdir(), "magnus_form_autosave.json")
            if os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    self.form_data = json.load(f)
                self.populate_form_fields()
        except Exception as e:
            print(f"Failed to load draft: {e}")
            
    def populate_form_fields(self):
        """Populate form fields with loaded data"""
        for object_name, value in self.form_data.items():
            widget = self.findChild((QLineEdit, QComboBox, QDateEdit, QTextEdit, QSpinBox, QCheckBox, QRadioButton), object_name)
            if widget:
                try:
                    if isinstance(widget, QLineEdit):
                        widget.setText(str(value))
                    elif isinstance(widget, QComboBox):
                        index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    elif isinstance(widget, QDateEdit):
                        widget.setDate(QDate.fromString(str(value), "MM/dd/yyyy"))
                    elif isinstance(widget, QTextEdit):
                        widget.setPlainText(str(value))
                    elif isinstance(widget, QSpinBox):
                        if value:
                            widget.setValue(int(value))
                    elif isinstance(widget, QCheckBox):
                        widget.setChecked(bool(value))
                    elif isinstance(widget, QRadioButton):
                        widget.setChecked(bool(value))
                except Exception as e:
                    print(f"Failed to populate field {object_name}: {e}")
                    
    def save_draft(self):
        """Save current form as draft"""
        self.collect_form_data()
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Draft", "magnus_form_draft.json", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.form_data, f, indent=2, default=str)
                QMessageBox.information(self, "Success", "Draft saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save draft: {e}")
                
    def generate_pdf_report(self):
        """Generate PDF report from form data"""
        self.collect_form_data()

        # Validate required fields
        form_validator.clear_errors()
        if not form_validator.validate_all_sections(self.form_data):
            errors = form_validator.get_error_summary()
            QMessageBox.warning(self, "Validation Errors", f"Please correct the following errors:\n\n{errors}")                     
            return

        # Get save location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", "Magnus_Client_Intake_Form.pdf", "PDF Files (*.pdf)"
        )

        if file_path:
            try:
                success = generate_pdf_from_data(self.form_data, file_path)
                if success:
                    QMessageBox.information(self, "Success", f"PDF report generated successfully!\n\nSaved to: {file_path}")
                    # Open the file
                    import subprocess
                    import platform
                    if platform.system() == 'Windows':
                        os.startfile(file_path)
                    elif platform.system() == 'Darwin':
                        subprocess.call(['open', file_path])
                    else:
                        subprocess.call(['xdg-open', file_path])
                else:
                    raise Exception("PDF generation returned False")

            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                QMessageBox.critical(self, "PDF Error", f"Failed to generate PDF:\n{e}\n\nDetails:\n{error_details}")



def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Magnus Client Intake Form")
    app.setApplicationVersion("2.2")
    
    # Set application style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ffffff;
        }
        QLabel {
            color: #2c3e50;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """)
    
    # Create and show main window
    window = MagnusClientIntakeForm()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())


