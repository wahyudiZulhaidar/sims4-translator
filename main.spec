# -*- mode: python ; coding: utf-8 -*-

import sys
import os

python_base_dir = sys.base_prefix
dlls_path = os.path.join(python_base_dir, 'DLLs')

ssl_dlls = [
    (os.path.join(dlls_path, 'libcrypto-3.dll'), '.'),
    (os.path.join(dlls_path, 'libssl-3.dll'), '.')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=ssl_dlls,
    datas=[('prefs', 'prefs')],
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
    [],
    exclude_binaries=True,
    name='translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/logo.ico',
    version='version.txt'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='build',
)