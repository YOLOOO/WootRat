# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['src'],
    binaries=[
        ('resources/wooting_analog_sdk.dll', 'resources')
    ],
    datas=[
        ('resources/woot_rat.png', 'resources'),
        ('resources/woot_rat.ico', 'resources'),
        ('utils/style.qss', 'utils'),
        ('utils/settings.json', 'utils'),
    ],
    hiddenimports=[
        'pynput.mouse',
        'ctypes',
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
    icon=['resources/woot_rat.ico']
)
