from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
    """Create the financial information page"""
    widget = QWidget()
    main_layout = QVBoxLayout(widget)

    # Page title
    title = QLabel("Financial Information")
    title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
    main_layout.addWidget(title)

    # Create scroll area
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)

    # Create content widget
    content_widget = QWidget()
    layout = QVBoxLayout(content_widget)

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
    layout.addWidget(QLabel("Estimated Tax Bracket:"))
    tax_bracket_combo = QComboBox()
    tax_bracket_combo.setObjectName("tax_bracket")
    tax_bracket_combo.addItems([
        "", "0-15%", "15%-32%", "32%+"
    ])
    tax_bracket_combo.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
    """)
    layout.addWidget(tax_bracket_combo)

    # Risk Tolerance
    layout.addWidget(QLabel("Investment Risk Tolerance:"))
    risk_combo = QComboBox()
    risk_combo.setObjectName("risk_tolerance")
    risk_combo.addItems([
        "", "Conservative", "Moderate", "Moderately Aggressive", "Aggressive"
    ])
    risk_combo.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
        }
    """)
    layout.addWidget(risk_combo)

    # Investment Purpose
    purpose_label = QLabel("Investment Purpose:")
    purpose_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
    layout.addWidget(purpose_label)

    purpose_group = QGroupBox()
    purpose_group.setStyleSheet("""
        QGroupBox {
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 5px;
            padding: 10px;
            background-color: #f8f9fa;
        }
        QCheckBox {
            spacing: 8px;
            font-size: 12px;
            padding: 5px;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #bdc3c7;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            background-color: #28a745;
            border-color: #28a745;
        }
    """)
    purpose_layout = QVBoxLayout(purpose_group)

    purpose_options = ["Income", "Growth and Income", "Capital Appreciation", "Speculation"]
    form.purpose_checkboxes = {}

    for purpose in purpose_options:
        checkbox = QCheckBox(purpose)
        checkbox.setObjectName(f"investment_purpose_{purpose.lower().replace(' ', '_')}")
        form.purpose_checkboxes[purpose] = checkbox
        purpose_layout.addWidget(checkbox)

    layout.addWidget(purpose_group)

    # Investment Objectives Ranking
    objectives_label = QLabel("Investment Objectives (Rank 1-5, where 1 is highest priority):")
    objectives_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
    layout.addWidget(objectives_label)

    objectives_group = QGroupBox()
    objectives_group.setStyleSheet("""
        QGroupBox {
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 5px;
            padding: 10px;
            background-color: #f8f9fa;
        }
        QSpinBox {
            padding: 8px;
            border: 2px solid #bdc3c7;
            border-radius: 4px;
            min-width: 80px;
            font-size: 12px;
        }
        QLabel {
            font-size: 12px;
            padding: 5px;
        }
    """)
    objectives_layout = QVBoxLayout(objectives_group)

    objectives = [
        "Trading Profits", "Speculation", "Capital Appreciation", 
        "Income", "Preservation of Capital"
    ]
    form.objective_spinboxes = {}

    for objective in objectives:
        h_layout = QHBoxLayout()
        label = QLabel(objective)
        label.setMinimumWidth(200)  # Ensure consistent label width
        spinbox = QSpinBox()
        spinbox.setObjectName(f"investment_objective_{objective.lower().replace(' ', '_')}")
        spinbox.setRange(1, 5)
        spinbox.setValue(3)  # Default to middle priority
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
            }
        """)

        form.objective_spinboxes[objective] = spinbox
        h_layout.addWidget(label)
        h_layout.addWidget(spinbox)
        h_layout.addStretch()
        objectives_layout.addLayout(h_layout)

    layout.addWidget(objectives_group)

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

    # Add the content widget to the scroll area
    scroll_area.setWidget(content_widget)
    main_layout.addWidget(scroll_area)

    # Navigation buttons
    main_layout.addLayout(form.create_navigation_buttons(back_index=3, next_index=5))

    form.stacked_widget.addWidget(widget)
