from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
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
        employment_combo.currentTextChanged.connect(form.on_employment_status_changed)
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
        form.retirement_group = QGroupBox("Retirement Information")
        form.retirement_group.setObjectName("retirement_group")
        form.retirement_group.setVisible(False)
        retirement_layout = QVBoxLayout(form.retirement_group)

        retirement_layout.addWidget(QLabel("Former Employer:"))
        former_employer_input = EnhancedLineEdit("former_employer")
        former_employer_input.setObjectName("former_employer")
        retirement_layout.addWidget(former_employer_input)

        retirement_layout.addWidget(QLabel("Source of Income:"))
        income_source_input = EnhancedLineEdit("income_source")
        income_source_input.setObjectName("income_source")
        retirement_layout.addWidget(income_source_input)

        layout.addWidget(form.retirement_group)

        layout.addStretch()
        layout.addLayout(form.create_navigation_buttons(back_index=2, next_index=4))

        form.stacked_widget.addWidget(widget)
