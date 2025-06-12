#!/usr/bin/env python3
"""
Enhanced Packaging Script for Magnus Client Intake Form Application - Version 2.0
Creates all necessary files for building a Windows installer with enhanced features.
"""

import os
import sys
import platform

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(SCRIPT_DIR, "icon.ico")
LICENSE_PATH = os.path.join(SCRIPT_DIR, "LICENSE.txt")
HOOK_PATH = os.path.join(SCRIPT_DIR, "hook.py")
BATCH_FILE_PATH = os.path.join(SCRIPT_DIR, "build_installer.bat")
REQUIREMENTS_PATH = os.path.join(SCRIPT_DIR, "requirements.txt")

# Create requirements.txt with all dependencies
requirements_content = """PyQt6>=6.4.0
reportlab>=3.6.0
cryptography>=3.4.8
"""

with open(REQUIREMENTS_PATH, "w") as f:
    f.write(requirements_content)
print(f"Created requirements.txt at {REQUIREMENTS_PATH}")

# Create LICENSE.txt if it doesn't exist
if not os.path.exists(LICENSE_PATH):
    with open(LICENSE_PATH, "w") as f:
        f.write("""Magnus Client Intake Form Application License - Enhanced Version

Copyright (c) 2025 Magnus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

ENHANCED FEATURES:
- Advanced form validation with real-time feedback
- Auto-save functionality and draft management
- Data encryption for sensitive information
- Accessibility features and keyboard navigation
- Professional PDF generation with comprehensive formatting
""")
    print(f"Created LICENSE.txt at {LICENSE_PATH}")

# Create enhanced hook.py
if not os.path.exists(HOOK_PATH):
    with open(HOOK_PATH, "w") as f:
        f.write("""import os
import sys

# Ensure PyQt6 can find its dependencies
if hasattr(sys, '_MEIPASS'):
    os.environ['QT_PLUGIN_PATH'] = os.path.join(sys._MEIPASS, 'PyQt6', 'Qt6', 'plugins')
    os.environ['QML2_IMPORT_PATH'] = os.path.join(sys._MEIPASS, 'PyQt6', 'Qt6', 'qml')
    
    # Add cryptography support
    os.environ['CRYPTOGRAPHY_DONT_BUILD_RUST'] = '1'
""")
    print(f"Created hook.py at {HOOK_PATH}")

# Create enhanced PyInstaller spec file
spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_enhanced.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE.txt', '.'), 
        ('pdf_generator_reportlab.py', '.'),
        ('validation.py', '.'),
        ('security.py', '.'),
        ('requirements.txt', '.')
    ],
    hiddenimports=[
        'PyQt6', 
        'PyQt6.QtWidgets', 
        'PyQt6.QtCore', 
        'PyQt6.QtGui',
        'reportlab.graphics.barcode', 
        'reportlab.graphics.barcode.code128', 
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.kdf.pbkdf2'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MagnusClientIntakeForm_Enhanced',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version_info={
        'version': '2.0.0.0',
        'description': 'Magnus Client Intake Form - Enhanced Version',
        'company': 'Magnus',
        'product': 'Magnus Client Intake Form',
        'copyright': 'Copyright (c) 2025 Magnus'
    }
)
"""

with open(os.path.join(SCRIPT_DIR, "magnus_form_enhanced.spec"), "w") as f:
    f.write(spec_content)
    print(f"Created PyInstaller spec file at {os.path.join(SCRIPT_DIR, 'magnus_form_enhanced.spec')}")

# Create enhanced NSIS installer script
nsis_content = """
; Magnus Client Intake Form Enhanced Installer Script
; Created with NSIS

!include "MUI2.nsh"

; Application information
Name "Magnus Client Intake Form Enhanced"
OutFile "MagnusClientIntakeForm_Enhanced_Setup.exe"
InstallDir "$PROGRAMFILES\\Magnus Client Intake Form Enhanced"
InstallDirRegKey HKCU "Software\\Magnus Client Intake Form Enhanced" ""

; Request application privileges
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header.bmp" ; Optional: Add header image
!define MUI_WELCOMEFINISHPAGE_BITMAP "welcome.bmp" ; Optional: Add welcome image

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer sections
Section "Magnus Client Intake Form Enhanced" SecMain
  SectionIn RO ; Required section
  SetOutPath "$INSTDIR"
  
  ; Add files
  File "dist\\MagnusClientIntakeForm_Enhanced.exe"
  File "LICENSE.txt"
  File "requirements.txt"
  
  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\\Magnus Client Intake Form Enhanced"
  CreateShortcut "$SMPROGRAMS\\Magnus Client Intake Form Enhanced\\Magnus Client Intake Form Enhanced.lnk" "$INSTDIR\\MagnusClientIntakeForm_Enhanced.exe"
  CreateShortcut "$DESKTOP\\Magnus Client Intake Form Enhanced.lnk" "$INSTDIR\\MagnusClientIntakeForm_Enhanced.exe"
  
  ; Write uninstaller
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  
  ; Write registry keys for uninstall
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced" "DisplayName" "Magnus Client Intake Form Enhanced"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced" "DisplayIcon" "$INSTDIR\\MagnusClientIntakeForm_Enhanced.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced" "Publisher" "Magnus"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced" "DisplayVersion" "2.0"
  WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced" "EstimatedSize" 50000
SectionEnd

Section "Desktop Shortcut" SecDesktop
  CreateShortcut "$DESKTOP\\Magnus Client Intake Form Enhanced.lnk" "$INSTDIR\\MagnusClientIntakeForm_Enhanced.exe"
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu
  CreateDirectory "$SMPROGRAMS\\Magnus Client Intake Form Enhanced"
  CreateShortcut "$SMPROGRAMS\\Magnus Client Intake Form Enhanced\\Magnus Client Intake Form Enhanced.lnk" "$INSTDIR\\MagnusClientIntakeForm_Enhanced.exe"
  CreateShortcut "$SMPROGRAMS\\Magnus Client Intake Form Enhanced\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
SectionEnd

; Descriptions
LangString DESC_SecMain ${LANG_ENGLISH} "Main application files (required)"
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create desktop shortcut"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "Create Start Menu shortcuts"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller section
Section "Uninstall"
  ; Remove files
  Delete "$INSTDIR\\MagnusClientIntakeForm_Enhanced.exe"
  Delete "$INSTDIR\\LICENSE.txt"
  Delete "$INSTDIR\\requirements.txt"
  Delete "$INSTDIR\\Uninstall.exe"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\\Magnus Client Intake Form Enhanced\\Magnus Client Intake Form Enhanced.lnk"
  Delete "$SMPROGRAMS\\Magnus Client Intake Form Enhanced\\Uninstall.lnk"
  Delete "$DESKTOP\\Magnus Client Intake Form Enhanced.lnk"
  RMDir "$SMPROGRAMS\\Magnus Client Intake Form Enhanced"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Magnus Client Intake Form Enhanced"
  
  ; Remove installation directory
  RMDir "$INSTDIR"
SectionEnd
"""

with open(os.path.join(SCRIPT_DIR, "installer_enhanced.nsi"), "w") as f:
    f.write(nsis_content)
    print(f"Created NSIS installer script at {os.path.join(SCRIPT_DIR, 'installer_enhanced.nsi')}")

# Create enhanced batch file for building the installer
batch_content = """@echo off
echo Starting Magnus Client Intake Form Enhanced installer build process...

echo Creating virtual environment...
python -m venv venv
call venv\\Scripts\\activate.bat

echo Installing required packages...
pip install -r requirements.txt
pip install pyinstaller

echo Building executable with PyInstaller...
pyinstaller magnus_form_enhanced.spec

echo Creating installer with NSIS...
"C:\\Program Files (x86)\\NSIS\\makensis.exe" installer_enhanced.nsi

echo Build process completed.
echo The installer should be available as MagnusClientIntakeForm_Enhanced_Setup.exe
echo.
echo Enhanced Features Included:
echo - Advanced form validation with real-time feedback
echo - Auto-save functionality and draft management  
echo - Data encryption for sensitive information
echo - Accessibility features and keyboard navigation
echo - Professional PDF generation
echo.
pause
"""

with open(BATCH_FILE_PATH, "w") as f:
    f.write(batch_content)
    print(f"Created batch file at {BATCH_FILE_PATH}")

# Create a simple icon file if it doesn't exist
if not os.path.exists(ICON_PATH):
    print(f"Note: Please add an icon file named 'icon.ico' to {SCRIPT_DIR}")
    print("You can create one online or use any .ico file for the application icon.")

# Create README for the enhanced version
readme_content = """# Magnus Client Intake Form - Enhanced Version 2.0

## Overview
This is an enhanced version of the Magnus Client Intake Form application with advanced features including validation, security, and accessibility improvements.

## New Features in Version 2.0

### Enhanced Validation
- Real-time field validation with visual feedback
- Comprehensive data consistency checks
- Professional error messaging
- Required field indicators

### Data Security
- Encryption for sensitive information (SSN, etc.)
- Secure temporary file handling
- Auto-save with encrypted storage
- Secure data deletion

### Accessibility
- Keyboard navigation support
- Screen reader compatibility
- Tooltips and help text
- Focus indicators

### User Experience
- Auto-save every 30 seconds
- Draft save/load functionality
- Progress tracking
- Professional styling

## System Requirements
- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space
- .NET Framework 4.7.2 or later

## Installation
1. Download MagnusClientIntakeForm_Enhanced_Setup.exe
2. Run as administrator
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

## Building from Source
1. Install Python 3.11 or later
2. Run build_installer.bat
3. Installer will be created as MagnusClientIntakeForm_Enhanced_Setup.exe

## Dependencies
- PyQt6 (GUI framework)
- ReportLab (PDF generation)
- Cryptography (Data encryption)

## Support
For technical support or questions, please contact the Magnus development team.

## Version History
- v2.0: Enhanced version with validation, security, and accessibility
- v1.0: Original basic version
"""

with open(os.path.join(SCRIPT_DIR, "README.md"), "w") as f:
    f.write(readme_content)
    print(f"Created README.md at {os.path.join(SCRIPT_DIR, 'README.md')}")

print("\nAll enhanced packaging files have been created successfully!")
print("\nEnhanced Features Included:")
print("✓ Advanced form validation with real-time feedback")
print("✓ Auto-save functionality and draft management")
print("✓ Data encryption for sensitive information")
print("✓ Accessibility features and keyboard navigation")
print("✓ Professional PDF generation")
print("\nTo build the enhanced installer:")
print("1. Make sure you have an icon file named 'icon.ico' in the same directory")
print("2. Run the batch file 'build_installer.bat'")
print("3. The installer will be created as 'MagnusClientIntakeForm_Enhanced_Setup.exe'")
print("\nNote: The enhanced version requires additional dependencies (cryptography)")
print("These will be automatically installed during the build process.")

