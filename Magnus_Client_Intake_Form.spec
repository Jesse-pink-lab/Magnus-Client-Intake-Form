# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

# Explicitly include required modules that aren't imported at build time
extra_datas = [
    ('magnus_app/pdf_generator_reportlab.py', 'magnus_app'),
    ('magnus_app/validation.py', 'magnus_app'),
    ('security.py', '.'),
]

a = Analysis(
    ['magnus_app/app.py'],
    pathex=['.'],
    binaries=[],
    datas=extra_datas,
    hiddenimports=[],
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
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['ICON.ico'],
)
