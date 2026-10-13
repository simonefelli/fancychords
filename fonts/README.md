# Fonts

FancyChords and FancyScales write the font **name** into the SVG files; the
font itself is taken from the computer that shows the image or converts it
to PNG. To get the same images everywhere, the font must be installed.

The default font is **`Ubuntu Mono derivative FChords`**: the Ubuntu Mono
font of ubuntu-font-family-0.83 with a new name, and nothing else changed.

## Install

Install the four `.ttf` files of
[ubuntu-mono-derivative-fchords](./ubuntu-mono-derivative-fchords), like any
other font:

- **Linux**:

  ```bash
  mkdir -p ~/.local/share/fonts
  cp fonts/ubuntu-mono-derivative-fchords/*.ttf ~/.local/share/fonts/
  fc-cache -f
  fc-match "Ubuntu Mono derivative FChords"   # must print UbuntuMonoderivativeFChords-R.ttf
  ```

- **Windows**: select the four `.ttf` files, right click, *Install for all
  users*.

Nothing else is needed: the programs use it by default, and it does not
change the fonts used by other programs.

## Why a renamed font

The chords are designed with Ubuntu Mono version 0.80, the one of the
ubuntu-font-family-0.83 release. Newer systems (ie Ubuntu 24.04 and later,
package `fonts-ubuntu` 0.869) have a newer Ubuntu Mono that draws bolder
and larger characters, with the same name. With its own name the 0.80 font
is always the one used, on any system, also when the newer Ubuntu Mono is
installed (checked by the tests).

The Ubuntu Font Licence allows this: a modified version (here, only the
name) must be named after the original with "derivative X" appended
(condition 2c), hence `Ubuntu Mono derivative FChords`.

Chords made with older versions of the programs use the name
`Ubuntu Mono Legacy` (a renamed copy of the same font that is not
distributed here); that name is still accepted by `--font-family`.

## Files

- [ubuntu-font-family-0.83](./ubuntu-font-family-0.83): the original Ubuntu
  font family release 0.83 by Canonical Ltd. and Dalton Maag Ltd.,
  **unmodified**, as downloaded from
  <https://assets.ubuntu.com/v1/0cef8205-ubuntu-font-family-0.83.zip> (only
  the `__MACOSX` folder of the zip archive was left out).
- [ubuntu-mono-derivative-fchords](./ubuntu-mono-derivative-fchords): the
  renamed font, made from the four `UbuntuMono-*.ttf` files of the original
  by [make_fchords_font.py](./make_fchords_font.py). Only the names change:
  family, full and PostScript names, plus a description of the change; the
  digital signature of the original files (`DSIG` table) is removed, as
  any change makes it invalid. The glyphs and all the other font data are
  byte-identical. Anyone can rebuild the files and compare them:

  ```bash
  pip install fonttools
  python3 fonts/make_fchords_font.py --check
  ```

## Licence

Both folders are under the **Ubuntu Font Licence 1.0**: see
[LICENCE.txt](./ubuntu-font-family-0.83/LICENCE.txt),
[copyright.txt](./ubuntu-font-family-0.83/copyright.txt) and
[TRADEMARKS.txt](./ubuntu-font-family-0.83/TRADEMARKS.txt) (also copied
next to the renamed font). The licence applies to the font files only, not
to the rest of this repository (GPL). "Ubuntu" and "Canonical" are
registered trademarks of Canonical Ltd.; the renamed font is not endorsed
by them.

## Checked by the tests

The GitHub Actions workflow:

1. rebuilds the renamed font from the original files and checks it is
   identical to the one in the repository;
2. installs it and draws the chords of
   [tests/reference_png/reference_chords.txt](../tests/reference_png/reference_chords.txt)
   with the packaged executable, using the default font and a font that
   does not exist: the images must differ (the font is really installed
   and used), on both Linux and Windows;
3. on Linux, the images must also look like the reference images in the
   same folder, made on Simone's computer (see
   [compare_png.py](../tests/reference_png/compare_png.py) for the
   tolerance);
4. on Linux, installs the fonts of Ubuntu 24.04 (`fonts-ubuntu` 0.869) too
   and draws the chords again: they must not change.
