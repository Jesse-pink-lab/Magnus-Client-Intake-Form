from PyQt6.QtWidgets import QLineEdit
from validation import form_validator

class EnhancedLineEdit(QLineEdit):
    """Enhanced QLineEdit with validation feedback"""

    def __init__(self, field_name: str, parent=None):
        super().__init__(parent)
        self.field_name = field_name
        self.setStyleSheet(
            """
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            """
        )

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
            self.setStyleSheet(
                """
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #f44336;
                    border-radius: 4px;
                    font-size: 12px;
                    background-color: #ffebee;
                }
                """
            )
        elif text and valid:
            self.setStyleSheet(
                """
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #4CAF50;
                    border-radius: 4px;
                    font-size: 12px;
                    background-color: #e8f5e8;
                }
                """
            )
        else:
            self.setStyleSheet(
                """
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #ddd;
                    border-radius: 4px;
                    font-size: 12px;
                }
                """
            )

        return valid
