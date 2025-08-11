if __package__ in (None, ""):
    import os, sys  # noqa: E401
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "magnus_app"
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
