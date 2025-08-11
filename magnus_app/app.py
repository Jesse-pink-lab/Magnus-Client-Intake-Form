import sys
from PyQt6.QtWidgets import QApplication

from magnus_app.main_window import MagnusClientIntakeForm


def main() -> None:
    app = QApplication(sys.argv)
    form = MagnusClientIntakeForm()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
