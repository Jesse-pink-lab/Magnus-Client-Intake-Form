import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from .main_window import MagnusClientIntakeForm


def _load_qss(app: QApplication) -> None:
    qss = Path(__file__).with_name("theme.qss")
    if qss.exists():
        app.setStyleSheet(qss.read_text(encoding="utf-8"))


def main() -> None:
    app = QApplication(sys.argv)
    _load_qss(app)
    form = MagnusClientIntakeForm()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
