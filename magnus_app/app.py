from __future__ import annotations

import os
import sys
import io
import platform
import datetime
import traceback
import logging
from pathlib import Path


_APP_NAME = "Magnus Client Intake"


def _user_log_dir() -> Path:
    """Return a user-writable directory for logs."""
    env = os.getenv("MAGNUS_LOG_DIR")
    if env:
        p = Path(env).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p
    if os.name == "nt":
        base = Path(os.getenv("LOCALAPPDATA", Path.home()))
        p = base / _APP_NAME / "Logs"
    else:
        base = Path(os.getenv("XDG_STATE_HOME", Path.home() / ".local" / "state"))
        p = base / _APP_NAME / "logs"
    try:
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        from tempfile import gettempdir
        q = Path(gettempdir()) / "MagnusLogs"
        q.mkdir(parents=True, exist_ok=True)
        return q


_LOG_DIR = _user_log_dir()
_LOG_PATH = _LOG_DIR / "crash.log"


def log_path() -> Path:
    """Path to the active crash log."""
    return _LOG_PATH


def _log(msg: str) -> None:
    """Append *msg* to the crash log, never raising."""
    try:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(msg)
            if not msg.endswith("\n"):
                f.write("\n")
            f.flush()
    except Exception:
        pass


def _rotate_if_large(limit_mb: int = 5) -> None:
    try:
        if _LOG_PATH.exists() and _LOG_PATH.stat().st_size > limit_mb * 1024 * 1024:
            ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            _LOG_PATH.rename(_LOG_PATH.with_name(f"crash-{ts}.log"))
    except Exception:
        pass


_rotate_if_large()


def _excepthook(exc_type, exc, tb):
    _log(f"[{datetime.datetime.now().isoformat()}] UNCAUGHT EXCEPTION")
    _log("".join(traceback.format_exception(exc_type, exc, tb)))
    try:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(
            None,
            "Unexpected error",
            f"The app hit an unexpected error and will close.\n\nCrash log:\n{_LOG_PATH}",
        )
    except Exception:
        pass


sys.excepthook = _excepthook


def _redirect_streams() -> None:
    try:
        if getattr(sys, "frozen", False):
            class _LogWriter(io.TextIOBase):
                def write(self, s):  # type: ignore[override]
                    if s:
                        _log(s.rstrip("\n"))
                    return len(s)

            sys.stdout = _LogWriter()  # type: ignore
            sys.stderr = _LogWriter()  # type: ignore
    except Exception:
        pass


_redirect_streams()


def install_qt_message_handler() -> None:
    try:
        from PyQt6.QtCore import qInstallMessageHandler, QtMsgType

        def handler(mode, context, message):
            lvl = {
                QtMsgType.QtDebugMsg: "DEBUG",
                QtMsgType.QtInfoMsg: "INFO",
                QtMsgType.QtWarningMsg: "WARN",
                QtMsgType.QtCriticalMsg: "CRITICAL",
                QtMsgType.QtFatalMsg: "FATAL",
            }.get(mode, "LOG")
            _log(f"[QT {lvl}] {message}")

        qInstallMessageHandler(handler)
    except Exception:
        pass


_log("=" * 72)
_log(f"Start: {datetime.datetime.now().isoformat()}")
_log(f"Log file: {_LOG_PATH}")
_log(f"Frozen: {getattr(sys, 'frozen', False)}  exe={getattr(sys, 'executable', '')}")
_log(f"Python: {platform.python_version()}  OS: {platform.platform()}")
_log(f"argv: {sys.argv}")

install_qt_message_handler()


def resource_path(*parts) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


def load_stylesheet(app) -> None:
    qss_path = resource_path("theme.qss")
    try:
        if not os.path.exists(qss_path):
            logging.warning("[QSS] Not found: %s", qss_path)
            return
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()
        if not qss.strip():
            logging.warning("[QSS] Empty stylesheet: %s", qss_path)
            return
        app.setStyleSheet(qss)
        logging.info("[QSS] Applied: %s (%d chars)", qss_path, len(qss))
    except Exception as e:
        logging.exception("[QSS] Failed to load %s: %s", qss_path, e)


def main() -> None:
    from PyQt6.QtGui import QPalette, QColor
    from PyQt6.QtWidgets import QApplication, QStyleFactory

    from .main_window import MagnusClientIntakeForm

    _log("[BOOT] main()")

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
    load_stylesheet(app)

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

