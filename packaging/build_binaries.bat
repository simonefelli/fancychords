@echo off
REM Build single file executables of fancychords and fancyscales with PyInstaller.
REM Run it from anywhere; the executables are written in dist\ (repo root).
REM
REM Needs: python with svgwrite, cairosvg and pyinstaller installed
REM (pip install svgwrite cairosvg pyinstaller) and the Cairo library (libcairo-2.dll).
REM Set VENV to use a virtualenv: set VENV=C:\path\to\venv

REM run from the repo root
cd /d "%~dp0.."
if defined VENV call "%VENV%\Scripts\activate.bat"

for %%p in (fancychords fancyscales) do (
    python -m PyInstaller --noconfirm --clean packaging\%%p.spec || exit /b 1
)

echo Job Done! Executables:
dir dist
