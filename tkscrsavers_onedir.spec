# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

import sys, os
sys.path.insert(0, os.getcwd())
hiddenimports = collect_submodules('screensavers')


a = Analysis(
    ['tkscrsavers.py'],
    pathex=['.', 'screensavers'],
    binaries=[('tkscrsvr.ico', '.'), ('settings.json', '.'), ('MS Mincho.ttf', '.'), ('tkscrsavers_log.txt', '.')],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='tkscrsavers',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['tkscrsvr.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='tkscrsavers',
)
