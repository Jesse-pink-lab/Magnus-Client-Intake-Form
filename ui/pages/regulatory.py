from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QComboBox,
    QDateEdit,
    QTextEdit,
    QCheckBox,
    QRadioButton,
    QButtonGroup,
    QSpinBox,
    QGroupBox,
    QScrollArea,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the regulatory consent page"""
    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Helper to add a yes/no question with proper object names
    def add_yes_no_question(parent_layout, question_text, object_prefix):
        label = QLabel(question_text)
        parent_layout.addWidget(label)
        group = QButtonGroup()
        yes = QRadioButton("Yes")
        yes.setObjectName(f"{object_prefix}_yes")
        group.addButton(yes)
        no = QRadioButton("No")
        no.setObjectName(f"{object_prefix}_no")
        group.addButton(no)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(yes)
        btn_layout.addWidget(no)
        parent_layout.addLayout(btn_layout)
        return group

    groupbox_style = """
        QGroupBox {
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
            background-color: #f8f9fa;
        }
        QRadioButton {
            spacing: 8px;
            font-size: 12px;
            padding: 5px;
        }
    """

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

    # Broker-Dealer Relationships
    broker_group = QGroupBox("Broker-Dealer Relationships")
    broker_group.setStyleSheet(groupbox_style)
    broker_layout = QVBoxLayout(broker_group)
    add_yes_no_question(
        broker_layout,
        "Employee of this Broker-Dealer?",
        "employee_this_broker_dealer",
    )
    add_yes_no_question(
        broker_layout,
        "Related to an Employee of this Broker-Dealer?",
        "related_employee_this_broker_dealer",
    )
    add_yes_no_question(
        broker_layout,
        "Employee of another Broker-Dealer?",
        "employee_another_broker_dealer",
    )
    add_yes_no_question(
        broker_layout,
        "Related to an employee of another Broker-Dealer?",
        "related_employee_another_broker_dealer",
    )
    layout.addWidget(broker_group)

    # Regulatory Affiliations
    reg_aff_group = QGroupBox("Regulatory Affiliations")
    reg_aff_group.setStyleSheet(groupbox_style)
    reg_aff_layout = QVBoxLayout(reg_aff_group)
    add_yes_no_question(
        reg_aff_layout,
        "Member of Stk Exch./FINRA?",
        "member_stock_exchange_finra",
    )
    add_yes_no_question(
        reg_aff_layout,
        "Are you a senior officer, director, or 10% or more shareholder of a public company?",
        "public_company_officer",
    )
    layout.addWidget(reg_aff_group)

    # Foreign Financial Accounts
    foreign_group = QGroupBox("Foreign Financial Accounts")
    foreign_group.setStyleSheet(groupbox_style)
    foreign_layout = QVBoxLayout(foreign_group)
    add_yes_no_question(
        foreign_layout,
        "Foreign Financial Institution Account?",
        "foreign_financial_institution_account",
    )
    add_yes_no_question(
        foreign_layout,
        "Is this a private banking account?",
        "private_banking_account",
    )
    add_yes_no_question(
        foreign_layout,
        "Is this an account for a Foreign Bank?",
        "foreign_bank_account",
    )
    layout.addWidget(foreign_group)

    # Politically Exposed Persons
    pep_group = QGroupBox("Politically Exposed Persons")
    pep_group.setStyleSheet(groupbox_style)
    pep_layout = QVBoxLayout(pep_group)
    add_yes_no_question(
        pep_layout,
        "Politically Exposed Person?",
        "politically_exposed_person",
    )
    layout.addWidget(pep_group)

    layout.addStretch()
    layout.addLayout(form.create_navigation_buttons(back_index=9, next_index=11))

    form.stacked_widget.addWidget(widget)
