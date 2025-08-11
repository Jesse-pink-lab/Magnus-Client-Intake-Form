import sys
from pathlib import Path
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtWidgets import QApplication
from .main_window import MagnusClientIntakeForm


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
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
