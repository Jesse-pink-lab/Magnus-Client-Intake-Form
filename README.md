# Magnus Client Intake Form

Simple PyQt6 application for capturing client intake information.

## Running

Install dependencies:

```
pip install -r requirements.txt
```

Run the application as a module:

```
python -m magnus_app.app
```

Or use the thin entry script:

```
python main_enhanced.py
```

## Building a standalone executable

From the repository root run:

```
pyinstaller --noconfirm --onefile --name Magnus_Client_Intake_Form ^
  --icon ICON.ico ^
  --collect-submodules PyQt6 --collect-data PyQt6 ^
  --add-data "ui;ui" --add-data "magnus_app;magnus_app" ^
  main_enhanced.py
```

This produces `dist/Magnus_Client_Intake_Form.exe` on Windows.  On macOS/Linux,
replace the `;` separators in the `--add-data` arguments with `:`.

The generated executable can be launched with:

```
./dist/Magnus_Client_Intake_Form.exe
```
