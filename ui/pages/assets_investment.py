from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
        """Create the assets and investment experience page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Page title
        title = QLabel("Assets & Investment Experience")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Create a scroll area for the entire content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        def _sync_scrollbar(_min=0, _max=0):
            policy = Qt.ScrollBarAlwaysOff if scroll_area.verticalScrollBar().maximum() == 0 else Qt.ScrollBarAsNeeded
            scroll_area.setVerticalScrollBarPolicy(policy)

        scroll_area.verticalScrollBar().rangeChanged.connect(_sync_scrollbar)

        # Create a widget to hold all the content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Asset Breakdown (optional)
        include_breakdown_checkbox = QCheckBox("Include Asset Breakdown")
        include_breakdown_checkbox.setObjectName("include_breakdown")
        include_breakdown_checkbox.stateChanged.connect(form.on_include_breakdown_changed)
        content_layout.addWidget(include_breakdown_checkbox)

        form.asset_breakdown_group = QGroupBox("Asset Breakdown")
        form.asset_breakdown_group.setObjectName("asset_breakdown_group")
        form.asset_breakdown_group.setVisible(False)

        breakdown_layout = QVBoxLayout(form.asset_breakdown_group)
        form.asset_breakdown_fields = {}

        asset_types = [
            "Stocks", "Bonds", "Mutual Funds", "ETFs", "UITs", 
            "Annuities (Fixed)", "Annuities (Variable)", "Options", 
            "Commodities", "Alternative Investments", "Limited Partnerships", 
            "Variable Contracts", "Short-Term", "Other"
        ]

        for asset_type in asset_types:
            h_layout = QHBoxLayout()
            label = QLabel(f"{asset_type} (%):")
            spin_box = QSpinBox()
            spin_box.setObjectName(f"asset_breakdown_{asset_type.lower().replace(' ', '_').replace('(', '').replace(')', '')}")
            spin_box.setRange(0, 100)
            spin_box.setSuffix("%")

            form.asset_breakdown_fields[asset_type] = spin_box
            h_layout.addWidget(label)
            h_layout.addWidget(spin_box)
            breakdown_layout.addLayout(h_layout)

        content_layout.addWidget(form.asset_breakdown_group)

        # Investment Experience by Asset Type
        experience_label = QLabel("Investment Experience by Asset Type:")
        experience_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        content_layout.addWidget(experience_label)

        # Create a scroll area specifically for investment experience
        experience_scroll = QScrollArea()
        experience_scroll.setWidgetResizable(True)
        experience_scroll.setFrameShape(QFrame.Shape.NoFrame)
        experience_scroll.setMinimumHeight(300)  # Set minimum height for better visibility

        def _sync_experience_scroll(_min=0, _max=0):
            policy = Qt.ScrollBarAlwaysOff if experience_scroll.verticalScrollBar().maximum() == 0 else Qt.ScrollBarAsNeeded
            experience_scroll.setVerticalScrollBarPolicy(policy)

        experience_scroll.verticalScrollBar().rangeChanged.connect(_sync_experience_scroll)

        experience_widget = QWidget()
        form.asset_experience_layout = QVBoxLayout(experience_widget)
        form.asset_experience_fields = {}

        experience_types = [
            "Stocks", "Bonds", "Mutual Funds", "UITs", 
            "Annuities (Fixed)", "Annuities (Variable)", "Options", 
            "Commodities", "Alternative Investments", "Limited Partnerships", 
            "Variable Contracts"
        ]

        for exp_type in experience_types:
            group_box = QGroupBox(exp_type)
            group_box.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #bdc3c7;
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
            group_box_layout = QHBoxLayout(group_box)

            year_label = QLabel("Year Started:")
            year_input = QLineEdit()
            year_input.setObjectName(f"asset_experience_{exp_type.lower().replace(' ', '_').replace('(', '').replace(')', '')}_year")
            year_input.setPlaceholderText("YYYY")
            year_input.setMaximumWidth(80)
            year_input.setStyleSheet("""
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #bdc3c7;
                    border-radius: 3px;
                }
            """)

            level_label = QLabel("Level:")
            level_combo = QComboBox()
            level_combo.setObjectName(f"asset_experience_{exp_type.lower().replace(' ', '_').replace('(', '').replace(')', '')}_level")
            level_combo.addItems(["", "None", "Limited", "Good", "Extensive"])
            level_combo.setStyleSheet("""
                QComboBox {
                    padding: 5px;
                    border: 1px solid #bdc3c7;
                    border-radius: 3px;
                }
            """)

            group_box_layout.addWidget(year_label)
            group_box_layout.addWidget(year_input)
            group_box_layout.addWidget(level_label)
            group_box_layout.addWidget(level_combo)
            group_box_layout.addStretch()

            form.asset_experience_fields[exp_type] = {"year": year_input, "level": level_combo}
            form.asset_experience_layout.addWidget(group_box)

        experience_scroll.setWidget(experience_widget)
        form.asset_experience_layout.addStretch()
        content_layout.addWidget(experience_scroll)

        # Outside Broker Firm
        has_outside_broker_checkbox = QCheckBox("Do you have assets with an outside broker firm?")
        has_outside_broker_checkbox.setObjectName("has_outside_broker")
        has_outside_broker_checkbox.stateChanged.connect(form.on_has_outside_broker_changed)
        content_layout.addWidget(has_outside_broker_checkbox)

        form.outside_broker_group = QGroupBox("Outside Broker Firm Information")
        form.outside_broker_group.setObjectName("outside_broker_group")
        form.outside_broker_group.setVisible(False)

        outside_broker_layout = QVBoxLayout(form.outside_broker_group)

        outside_broker_layout.addWidget(QLabel("Firm Name:"))
        outside_firm_name_input = EnhancedLineEdit("outside_firm_name")
        outside_firm_name_input.setObjectName("outside_firm_name")
        outside_broker_layout.addWidget(outside_firm_name_input)

        outside_broker_layout.addWidget(QLabel("Account Type:"))
        outside_account_type_input = QComboBox()
        outside_account_type_input.setObjectName("outside_broker_account_type")
        outside_account_type_input.addItems([
            "", "Individual", "Joint", "IRA", "Roth IRA", 
            "401(k)", "Trust", "Other"
        ])
        outside_broker_layout.addWidget(outside_account_type_input)

        outside_broker_layout.addWidget(QLabel("Account Number:"))
        outside_account_number_input = EnhancedLineEdit("outside_broker_account_number")
        outside_account_number_input.setObjectName("outside_broker_account_number")
        outside_broker_layout.addWidget(outside_account_number_input)

        outside_broker_layout.addWidget(QLabel("Liquid Amount with this Firm:"))
        outside_liquid_amount_input = EnhancedLineEdit("outside_liquid_amount")
        outside_liquid_amount_input.setObjectName("outside_liquid_amount")
        outside_liquid_amount_input.setPlaceholderText("Enter liquid amount in USD")
        outside_broker_layout.addWidget(outside_liquid_amount_input)

        content_layout.addWidget(form.outside_broker_group)
        content_layout.addStretch()

        # Add the content widget to the scroll area
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area, 1)

        # Navigation buttons
        layout.addLayout(form.create_navigation_buttons(back_index=7, next_index=9))

        form.stacked_widget.addWidget(widget)
