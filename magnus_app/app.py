import os
import sys
import traceback
import datetime
from pathlib import Path
from PyQt6.QtCore import qInstallMessageHandler, QtMsgType
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QStyleFactory, QMessageBox
from .main_window import MagnusClientIntakeForm


LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "crash.log")


def _log(msg: str) -> None:
    """Append *msg* to the crash log, ignoring any errors."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


def excepthook(exc_type, exc, tb):  # type: ignore[override]
    _log("UNCAUGHT EXCEPTION:\n" + "".join(traceback.format_exception(exc_type, exc, tb)))
    QMessageBox.critical(
        None,
        "Unexpected error",
        "The app hit an unexpected error and will close.\n\nSee crash.log for details.",
    )
    sys.__excepthook__(exc_type, exc, tb)
    sys.exit(1)


def qt_handler(mode: QtMsgType, context, message: str) -> None:  # type: ignore[override]
    _log(f"QT[{int(mode)}] {message}")


sys.excepthook = excepthook
qInstallMessageHandler(qt_handler)


def _load_qss(app: QApplication) -> None:
    qss = Path(__file__).with_name("theme.qss")
    if qss.exists():
        app.setStyleSheet(qss.read_text(encoding="utf-8"))


def main() -> None:
    app = QApplication(sys.argv)

    # Consistent, light baseline (prevents platform dark themes)
    app.setStyle(QStyleFactory.create("Fusion"))
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor("#f7f8fa"))
    pal.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    pal.setColor(QPalette.ColorRole.Text, QColor("#111827"))
    pal.setColor(QPalette.ColorRole.Button, QColor("#1677ff"))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
    app.setPalette(pal)
    _load_qss(app)

    form = MagnusClientIntakeForm()

    arg_paths = [a for a in sys.argv[1:] if os.path.isfile(a)]
    draft_path = next((p for p in arg_paths if p.lower().endswith((".mgd", ".json"))), None)

    if draft_path:
        try:
            form.open_draft_path(draft_path)
        except Exception:
            form.show_home()
    else:
        form.show_home()

    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
