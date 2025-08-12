@echo off
setlocal
set EXE="%~dp0dist\Magnus Client Intake Form.exe"
if not exist %EXE% (
  echo EXE not found at: %EXE%
  echo Build the app first so the exe exists under /dist.
  exit /b 1
)
set PROGID=MagnusClientIntake.Draft
reg add "HKCU\Software\Classes\.mgd" /ve /d "%PROGID%" /f
reg add "HKCU\Software\Classes\%PROGID%\DefaultIcon" /ve /d "%EXE%,0" /f
reg add "HKCU\Software\Classes\%PROGID%\shell\open\command" /ve /d "\"%~dp0dist\\Magnus Client Intake Form.exe\" \"%%1\"" /f
echo .mgd files now open with: %EXE%
endlocal
