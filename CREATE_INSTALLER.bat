@echo off
echo ============================================
echo Magnus Client Intake Form - Installer Creator
echo ============================================
echo.

echo Step 1: Installing Python dependencies...
pip install PyQt6 reportlab cryptography pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 2: Creating .exe file...
pyinstaller Magnus_Client_Intake_Form.spec
if %errorlevel% neq 0 (
    echo ERROR: Failed to create .exe file
    echo Trying alternative method...
    pyinstaller --onefile --windowed --icon=ICON.ico --name="Magnus_Client_Intake_Form" main_enhanced.py
    if %errorlevel% neq 0 (
        echo ERROR: Both methods failed
        pause
        exit /b 1
    )
)
echo .exe file created successfully!
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

