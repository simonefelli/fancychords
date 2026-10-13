FancyChords and FancyScales @VERSION@ (@PLATFORM@)
====================================================

FancyChords draws nice looking guitar chord diagrams, FancyScales does the
same for scales. Both write SVG images, and PNG copies with --convert.
Home page, full documentation and source code:
https://github.com/simonefelli/fancychords

Contents
--------
  @FANCYCHORDS@     the chords program
  @FANCYSCALES@     the scales program
  font/                the font used by the diagrams (see 1. below)
  examples/            example scale file and config file
  LICENSE              GNU General Public License version 3

1. Install the font (once)
--------------------------
The diagrams use the font "Ubuntu Mono derivative FChords". Install the
four .ttf files of the font/ folder, like any other font:

  - Windows: select the four .ttf files, right click, "Install for all users"
  - Linux:   mkdir -p ~/.local/share/fonts
             cp font/*.ttf ~/.local/share/fonts/
             fc-cache -f

Without it, another font is used and the labels look different.

2. Try it
---------
Open a terminal (Windows: Command Prompt or PowerShell) in this folder.

Draw a chord (name|frets|fingers|labels, one string per comma, from the
low E string):

  Linux:   ./fancychords --cli_in="C Major|x,3,2,0,1,0|x,3,2,x,1,x|x,R,3,5,R,3" --convert
  Windows: .\fancychords.exe --cli_in="C Major|x,3,2,0,1,0|x,3,2,x,1,x|x,R,3,5,R,3" --convert

Draw a scale (the A minor blues scale, D form of the CAGED system):

  Linux:   ./fancyscales examples/d_form.txt --config_file=examples/config_scales.json --convert
  Windows: .\fancyscales.exe examples\d_form.txt --config_file=examples\config_scales.json --convert

The images are written in the current folder, the PNG copies in png/.
All the options: --help, and the documentation on the home page.

Requirements
------------
  - Linux: x86_64 with glibc 2.35 or newer (ie Ubuntu 22.04, Debian 12 or
    newer). Python is not needed.
  - Windows: 64 bit Windows 10 or newer. Python is not needed.

Licence
-------
FancyChords and FancyScales: Copyright (C) 2026 Simone Felli, free software
under the GNU General Public License version 3 or (at your option) any
later version, see LICENSE. The source code of this version is on the home
page (tag @VERSION@).

The font in font/ is Ubuntu Mono 0.80 by Canonical Ltd. and Dalton Maag
Ltd., renamed as the Ubuntu Font Licence 1.0 asks for modified versions
(only the name was changed), see font/LICENCE.txt.
