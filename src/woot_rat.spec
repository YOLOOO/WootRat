# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['WootRatGui.py'],  # Main entry point
    pathex=['src'],  # Add the source directory to the path
    binaries=[
        ('resources/wooting_analog_sdk.dll', 'resources')
    ],
    datas=[
        ('resources/WootRat.png', 'icon'),
        ('resources/WootRat.ico', 'ico'),
        ('utils/style.qss', '.'),
        ('utils/settings.json', '.'),
    ],
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
    name='WootRat',
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
    icon=['resources/WootRat.ico']
)
