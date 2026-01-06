# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['Flash_Cards_main_v8.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images')],
    hiddenimports=[
        'numpy',
        'pkg_resources.py2_warn',
        'pkg_resources.extern',
        'pandas._libs.tslibs.timedeltas',
        'charset_normalizer',
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
    name='Flash_Cards_main_v8',
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
    icon=['images\\icon.ico'],
    # Output directly to dist folder, not subfolder
    distpath='dist',
)