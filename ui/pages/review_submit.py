from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QComboBox, QDateEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ui.widgets.enhanced_line_edit import EnhancedLineEdit

def create_page(form):
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
            form.review_area = QTextEdit()
            form.review_area.setReadOnly(True)
            form.review_area.setStyleSheet("""
                QTextEdit {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: monospace;
                    font-size: 11px;
                }
            """)
            layout.addWidget(form.review_area)

            # Action buttons
            button_layout = QHBoxLayout()

            save_draft_btn = QPushButton("Save Draft")
            save_draft_btn.clicked.connect(form.save_draft)
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
            generate_pdf_btn.clicked.connect(form.generate_pdf_report)
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
            layout.addLayout(form.create_navigation_buttons(back_index=10, next_index=None))

            form.stacked_widget.addWidget(widget)
