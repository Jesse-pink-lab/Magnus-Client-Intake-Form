# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

pyqt6_datas = collect_data_files("PyQt6")
pyqt6_hidden = collect_submodules("PyQt6")

a = Analysis(
    ['main_enhanced.py'],
    pathex=['.'],
    binaries=[],
    datas=pyqt6_datas + [
        ('ui', 'ui'),
        ('magnus_app', 'magnus_app'),
        ('security.py', '.'),
    ],
    hiddenimports=pyqt6_hidden + [
        'magnus_app.pages',
        'magnus_app.state',
        'magnus_app.renderer',
        'magnus_app.validation',
        'magnus_app.main_window',
        'magnus_app.app',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Magnus_Client_Intake_Form',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=['ICON.ico'],
)
