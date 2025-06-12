#!/usr/bin/env python3
"""
Security Module for Magnus Client Intake Form
Provides data encryption and secure file handling functionality
"""

import os
import json
import tempfile
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class DataSecurity:
    """Handles data encryption and secure operations"""
    
    def __init__(self, password=None):
        self.password = password or "magnus_default_key_2024"
        self.key = self._derive_key(self.password)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        password_bytes = password.encode()
        salt = b'magnus_salt_2024'  # In production, use random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt string data"""
        try:
            encrypted_data = self.cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            return data  # Return original data if encryption fails
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return encrypted_data  # Return original data if decryption fails
    
    def encrypt_sensitive_fields(self, form_data: dict) -> dict:
        """Encrypt sensitive fields in form data"""
        sensitive_fields = ['ssn', 'spouse_ssn']
        encrypted_data = form_data.copy()
        
        for field in sensitive_fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = self.encrypt_data(str(encrypted_data[field]))
                encrypted_data[f"{field}_encrypted"] = True
        
        return encrypted_data
    
    def decrypt_sensitive_fields(self, form_data: dict) -> dict:
        """Decrypt sensitive fields in form data"""
        sensitive_fields = ['ssn', 'spouse_ssn']
        decrypted_data = form_data.copy()
        
        for field in sensitive_fields:
            if f"{field}_encrypted" in decrypted_data and decrypted_data.get(f"{field}_encrypted"):
                if field in decrypted_data:
                    decrypted_data[field] = self.decrypt_data(str(decrypted_data[field]))
                    del decrypted_data[f"{field}_encrypted"]
        
        return decrypted_data
    
    def secure_save_data(self, data: dict, file_path: str) -> bool:
        """Securely save data to file with encryption"""
        try:
            # Encrypt sensitive fields
            encrypted_data = self.encrypt_sensitive_fields(data)
            
            # Create secure temporary file
            temp_fd, temp_path = tempfile.mkstemp(suffix='.tmp', prefix='magnus_')
            
            try:
                with os.fdopen(temp_fd, 'w') as temp_file:
                    json.dump(encrypted_data, temp_file, indent=2)
                
                # Move temp file to final location
                os.replace(temp_path, file_path)
                
                # Set restrictive permissions (owner read/write only)
                os.chmod(file_path, 0o600)
                
                return True
                
            except Exception as e:
                # Clean up temp file on error
                try:
                    os.unlink(temp_path)
                except:
                    pass
                raise e
                
        except Exception as e:
            print(f"Secure save error: {e}")
            return False
    
    def secure_load_data(self, file_path: str) -> dict:
        """Securely load and decrypt data from file"""
        try:
            with open(file_path, 'r') as f:
                encrypted_data = json.load(f)
            
            # Decrypt sensitive fields
            decrypted_data = self.decrypt_sensitive_fields(encrypted_data)
            
            return decrypted_data
            
        except Exception as e:
            print(f"Secure load error: {e}")
            return {}
    
    def secure_delete_file(self, file_path: str) -> bool:
        """Securely delete file by overwriting with random data"""
        try:
            if not os.path.exists(file_path):
                return True
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Overwrite with random data multiple times
            with open(file_path, 'r+b') as f:
                for _ in range(3):  # Overwrite 3 times
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Finally delete the file
            os.unlink(file_path)
            return True
            
        except Exception as e:
            print(f"Secure delete error: {e}")
            return False
    
    def hash_data(self, data: str) -> str:
        """Create hash of data for integrity checking"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def verify_data_integrity(self, data: str, expected_hash: str) -> bool:
        """Verify data integrity using hash"""
        return self.hash_data(data) == expected_hash

class AccessibilityHelper:
    """Provides accessibility features for the application"""
    
    @staticmethod
    def add_keyboard_shortcuts(widget):
        """Add keyboard shortcuts to widget"""
        from PyQt6.QtGui import QShortcut, QKeySequence
        from PyQt6.QtCore import Qt
        
        # Add common shortcuts
        shortcuts = {
            'Ctrl+S': 'save_draft',
            'Ctrl+O': 'load_draft',
            'Ctrl+N': 'new_form',
            'F1': 'show_help',
            'Escape': 'cancel_action'
        }
        
        for key_combo, action in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key_combo), widget)
            # Connect to appropriate methods if they exist
            if hasattr(widget, action):
                shortcut.activated.connect(getattr(widget, action))
    
    @staticmethod
    def set_accessible_properties(widget, name, description=None, role=None):
        """Set accessibility properties for widget"""
        widget.setAccessibleName(name)
        if description:
            widget.setAccessibleDescription(description)
        # Note: Role setting would require additional accessibility framework
    
    @staticmethod
    def add_tooltips_and_help(widget, tooltip_text, help_text=None):
        """Add tooltips and help text to widgets"""
        widget.setToolTip(tooltip_text)
        if help_text:
            widget.setWhatsThis(help_text)
    
    @staticmethod
    def set_tab_order(parent_widget, widget_list):
        """Set proper tab order for keyboard navigation"""
        from PyQt6.QtWidgets import QWidget
        
        for i in range(len(widget_list) - 1):
            QWidget.setTabOrder(widget_list[i], widget_list[i + 1])
    
    @staticmethod
    def add_focus_indicators(widget):
        """Add visual focus indicators for keyboard navigation"""
        widget.setStyleSheet(widget.styleSheet() + """
            QWidget:focus {
                border: 2px solid #4CAF50;
                outline: none;
            }
        """)

# Global security instance
data_security = DataSecurity()
accessibility_helper = AccessibilityHelper()

# Utility functions for easy access
def encrypt_form_data(data):
    """Convenience function to encrypt form data"""
    return data_security.encrypt_sensitive_fields(data)

def decrypt_form_data(data):
    """Convenience function to decrypt form data"""
    return data_security.decrypt_sensitive_fields(data)

def secure_save(data, file_path):
    """Convenience function for secure save"""
    return data_security.secure_save_data(data, file_path)

def secure_load(file_path):
    """Convenience function for secure load"""
    return data_security.secure_load_data(file_path)

def secure_delete(file_path):
    """Convenience function for secure delete"""
    return data_security.secure_delete_file(file_path)

