# Fonts

FancyChords and FancyScales write the font **name** into the SVG files
(default `Ubuntu Mono Legacy`); the font itself is taken from the computer
that shows the image or converts it to PNG. To get the same images
everywhere, the font must be installed.

## ubuntu-font-family-0.83

[ubuntu-font-family-0.83](./ubuntu-font-family-0.83) is the official
Ubuntu font family release 0.83 by Canonical Ltd. and Dalton Maag Ltd.,
**unmodified**, as downloaded from
<https://assets.ubuntu.com/v1/0cef8205-ubuntu-font-family-0.83.zip>
(only the `__MACOSX` folder of the zip archive was left out).

It is distributed under the **Ubuntu Font Licence 1.0**: see
[LICENCE.txt](./ubuntu-font-family-0.83/LICENCE.txt),
[copyright.txt](./ubuntu-font-family-0.83/copyright.txt) and
[TRADEMARKS.txt](./ubuntu-font-family-0.83/TRADEMARKS.txt). The licence
applies to the font files only, not to the rest of this repository (GPL).
"Ubuntu" and "Canonical" are registered trademarks of Canonical Ltd.

## Ubuntu Mono and "Ubuntu Mono Legacy"

The chords use **Ubuntu Mono** (`UbuntuMono-R.ttf`, `-B`, `-RI`, `-BI`;
version 0.80, unchanged in the 0.83 release) under the name
`Ubuntu Mono Legacy`. That name comes from a local copy of the same font
converted with FontForge and renamed, so it can be installed next to the
newer Ubuntu Mono of recent Ubuntu releases. That renamed copy is not
included here: the licence (condition 2) requires modified versions to be
named "Ubuntu Mono derivative ...", so only the original files are
distributed. They draw the same characters with the same sizes.

To use the original font with the name of the SVG files, map the name:

- **Linux** (fontconfig): install the fonts and the alias file
  [60-ubuntu-mono-legacy.conf](./60-ubuntu-mono-legacy.conf):

  ```bash
  mkdir -p ~/.local/share/fonts/ubuntu-font-family-0.83 ~/.config/fontconfig/conf.d
  cp fonts/ubuntu-font-family-0.83/UbuntuMono-*.ttf ~/.local/share/fonts/ubuntu-font-family-0.83/
  cp fonts/60-ubuntu-mono-legacy.conf ~/.config/fontconfig/conf.d/
  fc-cache -f
  fc-match "Ubuntu Mono Legacy"      # must print UbuntuMono-R.ttf: "Ubuntu Mono" "Regular"
  ```

- **Windows**: install the four `UbuntuMono-*.ttf` files (right click,
  *Install for all users*), and choose `Ubuntu Mono` as font: with
  `--font-family "Ubuntu Mono"` on the command line, or `"font_family":
  "Ubuntu Mono"` in a config file.

## Checked by the tests

The GitHub Actions workflow installs these fonts and draws the chords of
[tests/reference_png/reference_chords.txt](../tests/reference_png/reference_chords.txt);
the PNG images must match the reference images in the same folder, made
on Simone's computer with the original "Ubuntu Mono Legacy" setup (see
[compare_png.py](../tests/reference_png/compare_png.py) for how they are
compared). Checked on 583 chords: the original font and the renamed copy
give the same images, apart from the anti-aliasing of the text edges that
also changes between computers.
