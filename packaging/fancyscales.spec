# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec file: build a single file fancyscales executable.
# The same file works on Windows and Linux (no absolute paths):
#
#     pyinstaller packaging/fancyscales.spec
#
# or use packaging/build_binaries.sh / build_binaries.bat, that build
# both programs. The executable is written in dist/.
#
# Notes:
# - cairosvg / cairocffi (png conversion) are found by the PyInstaller
#   hooks (pyinstaller-hooks-contrib): they also bundle the system Cairo
#   library (libcairo.so.2 on Linux, libcairo-2.dll on Windows), which
#   must be installed on the build machine
# - PyInstaller does not cross compile: build the Windows executable on
#   Windows and the Linux one on Linux. A Linux executable runs on
#   distributions with the same or a newer glibc than the build machine
# - the 'block_cipher' / 'cipher' options of older spec files were
#   removed in PyInstaller 6 and are not used here

import os

# SPECPATH (set by PyInstaller) is the dir of this file: the repo root is its parent
repo_root = os.path.dirname(SPECPATH)

a = Analysis(
    [os.path.join(repo_root, 'fancyscales.py')],
    pathex=[repo_root],
    binaries=[],
    datas=[],
    # libs imported only inside functions are found anyway, these are
    # listed to be sure the png conversion is always included
    hiddenimports=['cairosvg', 'cairocffi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # not used by the programs, but pulled in as optional dependencies of
    # Pillow (used by cairosvg): excluding them makes the executable
    # about 40% smaller (21 MB instead of 36 MB on Linux)
    excludes=['numpy', 'tkinter', 'PIL.ImageTk', 'PIL.ImageQt'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='fancyscales',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # upx compression is off: it saves little and some antivirus programs
    # flag upx compressed executables
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
