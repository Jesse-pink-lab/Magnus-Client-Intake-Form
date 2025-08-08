from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
        """Create the dependents information page"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Page title
        title = QLabel("Dependents Information")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Dependents list container
        form.dependents_layout = QVBoxLayout()
        form.dependents_layout.setSpacing(10)

        form.dependents_scroll_area = QScrollArea()
        form.dependents_scroll_area.setWidgetResizable(True)
        form.dependents_scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        dependents_container = QWidget()
        dependents_container.setLayout(form.dependents_layout)
        form.dependents_scroll_area.setWidget(dependents_container)

        layout.addWidget(form.dependents_scroll_area)

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
        add_dependent_btn.clicked.connect(form.add_dependent_field)
        layout.addWidget(add_dependent_btn)

        layout.addStretch()
        layout.addLayout(form.create_navigation_buttons(back_index=5, next_index=7))

        form.stacked_widget.addWidget(widget)
