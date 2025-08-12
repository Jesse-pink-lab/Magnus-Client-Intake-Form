"""Thin wrapper for the Magnus Client Intake Form application.

This script allows running the app directly or packaging it with PyInstaller.
"""
from magnus_app.app import _log, log_path, main


_log("[BOOT] Entry script started")


if __name__ == "__main__":
    main()
