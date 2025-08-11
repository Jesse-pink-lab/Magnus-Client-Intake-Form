@echo off
echo ============================================
echo Magnus Client Intake Form - Installer Creator
echo ============================================
echo.

echo Step 1: Installing Python dependencies...
pip install PyQt6 reportlab python-docx cryptography pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 2: Creating .exe file...
if exist dist rd /s /q dist
pyinstaller --noconfirm --onefile --noconsole --name Magnus_Client_Intake_Form ^
  --icon ICON.ico ^
  --collect-submodules PyQt6 --collect-data PyQt6 ^
  --add-data "ui;ui" --add-data "magnus_app;magnus_app" ^
  main_enhanced.py

if exist "%~dp0dist\Magnus_Client_Intake_Form.exe" (
    echo .exe file created successfully!
) else (
    echo ERROR: Failed to create .exe file
    pause
    exit /b 1
)
echo.

echo Step 3: Creating professional installer...
makensis magnus_installer.nsi
if %errorlevel% neq 0 (
    echo WARNING: NSIS installer creation failed
    echo Make sure NSIS is installed and in PATH
    echo You can still use the .exe file in the dist folder
) else (
    echo Professional installer created successfully!
)
echo.

echo ============================================
echo COMPLETED!
echo ============================================
echo Your files are ready:
echo - Application: dist\Magnus_Client_Intake_Form.exe
echo - Installer: Magnus_Client_Intake_Form_Installer.exe
echo.
pause

