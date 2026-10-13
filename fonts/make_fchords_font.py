# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Simone Felli
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


"""
make_fchords_font: build the 'Ubuntu Mono derivative FChords' font files
(fonts/ubuntu-mono-derivative-fchords/) from the original Ubuntu Mono 0.80
files of ubuntu-font-family-0.83 (fonts/ubuntu-font-family-0.83/).

Only the font names change, the glyphs are untouched:
    - family names (name ids 1, 4, 16, 18): 'Ubuntu Mono'
      -> 'Ubuntu Mono derivative FChords', as the Ubuntu Font Licence 1.0
      (condition 2c) asks for modified versions
    - unique id (3) and PostScript name (6) follow the new name
    - a description (10) says what was changed
    - the DSIG table (digital signature of the original files) is removed,
      as it is no longer valid after any change
The output is always the same (no new timestamp), so anyone can rebuild the
files and compare them with the ones in the repository:

    pip install fonttools
    python3 fonts/make_fchords_font.py            # writes the files
    python3 fonts/make_fchords_font.py --check    # only compares, exit 1 if different
"""

# standard library imports
import os
import sys
import io

# third party imports
from fontTools.ttLib import TTFont


FONT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(FONT_DIR, 'ubuntu-font-family-0.83')
DST_DIR = os.path.join(FONT_DIR, 'ubuntu-mono-derivative-fchords')

OLD_FAMILY = 'Ubuntu Mono'
NEW_FAMILY = 'Ubuntu Mono derivative FChords'
# file name style suffix of the original files
STYLES = ['R', 'B', 'RI', 'BI']
# licence files that must go with every copy of the font (condition 1)
LICENCE_FILES = ['LICENCE.txt', 'copyright.txt', 'TRADEMARKS.txt']

DESCRIPTION = ('Ubuntu Mono 0.80 (ubuntu-font-family-0.83) renamed '
               '"Ubuntu Mono derivative FChords" for the FancyChords and '
               'FancyScales programs; only the font names were changed. '
               'Licensed under the Ubuntu Font Licence 1.0.')


def rename_font(src_path):
    '''
    load an original Ubuntu Mono file, change its names and return
    the new font file content (bytes)
    '''
    font = TTFont(src_path, recalcTimestamp=False)
    name = font['name']
    style = name.getDebugName(2)                       # ie 'Bold Italic'
    ps_family = NEW_FAMILY.replace(' ', '')
    for rec in name.names:
        old = rec.toUnicode()
        if rec.nameID in (1, 16, 18):                  # family names
            new = old.replace(OLD_FAMILY, NEW_FAMILY)
        elif rec.nameID == 4:                          # full name
            new = old.replace(OLD_FAMILY, NEW_FAMILY)
        elif rec.nameID == 3:                          # unique id
            new = old.replace(OLD_FAMILY, NEW_FAMILY)
        elif rec.nameID == 6:                          # PostScript name
            new = ps_family + '-' + style.replace(' ', '')
        else:
            continue
        rec.string = new
    # a description of the change, for both platforms of the original
    for plat, enc, lang in {(r.platformID, r.platEncID, r.langID) for r in name.names}:
        name.setName(DESCRIPTION, 10, plat, enc, lang)
    if 'DSIG' in font:
        del font['DSIG']
    out = io.BytesIO()
    font.save(out)
    return out.getvalue()


def main(check_only=False):
    '''
    build (or check, with check_only) all the files of DST_DIR,
    return the number of files that differ
    '''
    differ = 0
    os.makedirs(DST_DIR, exist_ok=True)
    targets = {}
    for st in STYLES:
        src = os.path.join(SRC_DIR, 'UbuntuMono-' + st + '.ttf')
        dst = os.path.join(DST_DIR, NEW_FAMILY.replace(' ', '') + '-' + st + '.ttf')
        targets[dst] = rename_font(src)
    for lf in LICENCE_FILES:
        with open(os.path.join(SRC_DIR, lf), 'rb') as f:
            targets[os.path.join(DST_DIR, lf)] = f.read()
    for dst, data in targets.items():
        old = None
        if os.path.exists(dst):
            with open(dst, 'rb') as f:
                old = f.read()
        if old == data:
            print('same     ', os.path.relpath(dst, FONT_DIR))
            continue
        differ += 1
        if check_only:
            print('DIFFERENT', os.path.relpath(dst, FONT_DIR))
        else:
            with open(dst, 'wb') as f:
                f.write(data)
            print('written  ', os.path.relpath(dst, FONT_DIR))
    return differ


if __name__ == '__main__':
    check = '--check' in sys.argv[1:]
    n = main(check_only=check)
    sys.exit(1 if (check and n) else 0)
