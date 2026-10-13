#!/bin/bash
# Build single file executables of fancychords and fancyscales with PyInstaller.
# Run it from anywhere; the executables are written in dist/ (repo root).
#
# Needs: python3 with svgwrite, cairosvg and pyinstaller installed
# (pip install svgwrite cairosvg pyinstaller) and the Cairo library.
# Set VENV to use a virtualenv: VENV=/path/to/venv ./build_binaries.sh

# run from the repo root
cd "$(dirname "$0")/.." || exit 1
if [ -n "$VENV" ] && [ -f "$VENV/bin/activate" ]; then source "$VENV/bin/activate"; fi

set -e
for prog in fancychords fancyscales; do
    python3 -m PyInstaller --noconfirm --clean packaging/$prog.spec
done

echo 'Job Done! Executables:'
ls -l dist/
