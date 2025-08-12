from __future__ import annotations
import os, sys, io, platform, datetime, traceback
from pathlib import Path

_APP_NAME = "Magnus Client Intake"


def _user_log_dir() -> Path:
    # Allow override
    env = os.getenv("MAGNUS_LOG_DIR")
    if env:
        p = Path(env).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p
    # Windows: LOCALAPPDATA\Magnus Client Intake\Logs
    if os.name == "nt":
        base = Path(os.getenv("LOCALAPPDATA", Path.home()))
        p = base / f"{_APP_NAME}" / "Logs"
    else:
        # ~/.local/state/Magnus Client Intake/logs (or fallback)
        base = Path(os.getenv("XDG_STATE_HOME", Path.home() / ".local" / "state"))
        p = base / f"{_APP_NAME}" / "logs"
    try:
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        # Fallback to temp
        from tempfile import gettempdir
        q = Path(gettempdir()) / "MagnusLogs"
        q.mkdir(parents=True, exist_ok=True)
        return q


_LOG_DIR = _user_log_dir()
_LOG_PATH = _LOG_DIR / "crash.log"


def log_path() -> Path:
    return _LOG_PATH


def _log(msg: str) -> None:
    try:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(msg)
            if not msg.endswith("\n"):
                f.write("\n")
            f.flush()
    except Exception:
        # never raise from logger
        pass


def _rotate_if_large(limit_mb: int = 5) -> None:
    try:
        if _LOG_PATH.exists() and _LOG_PATH.stat().st_size > limit_mb * 1024 * 1024:
            ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            _LOG_PATH.rename(_LOG_PATH.with_name(f"crash-{ts}.log"))
    except Exception:
        pass


_rotate_if_large()


# Capture ANY uncaught exception very early
def _excepthook(exc_type, exc, tb):
    _log(f"[{datetime.datetime.now().isoformat()}] UNCAUGHT EXCEPTION")
    _log("".join(traceback.format_exception(exc_type, exc, tb)))
    # Try to show a dialog; if UI not ready this will be a no-op.
    try:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(
            None,
            "Unexpected error",
            f"The app hit an unexpected error and will close.\n\n"
            f"Crash log:\n{_LOG_PATH}",
        )
    except Exception:
        pass
    # Let Qt/OS handle shutdown; don't sys.exit() here.


sys.excepthook = _excepthook


# Redirect stdout/stderr when running frozen (no console)
def _redirect_streams():
    try:
        if getattr(sys, "frozen", False):
            class _LogWriter(io.TextIOBase):
                def write(self, s):
                    if s:
                        _log(s.rstrip("\n"))
                    return len(s)

            sys.stdout = _LogWriter()  # type: ignore
            sys.stderr = _LogWriter()  # type: ignore
    except Exception:
        pass


_redirect_streams()


# Qt message handler hook
def install_qt_message_handler():
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


# Log environment at import time
_log("=" * 72)
_log(f"Start: {datetime.datetime.now().isoformat()}")
_log(f"Log file: {_LOG_PATH}")
_log(f"Frozen: {getattr(sys, 'frozen', False)}  exe={getattr(sys, 'executable', '')}")
_log(f"Python: {platform.python_version()}  OS: {platform.platform()}")
_log(f"argv: {sys.argv}")

install_qt_message_handler()


from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QStyleFactory

from .main_window import MagnusClientIntakeForm


def _load_qss(app: QApplication) -> None:
    qss = Path(__file__).with_name("theme.qss")
    if qss.exists():
        app.setStyleSheet(qss.read_text(encoding="utf-8"))


def main() -> None:
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
    _load_qss(app)
    form = MagnusClientIntakeForm()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
