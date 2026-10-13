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
Compare png chord images with the reference images in this folder.

    python compare_png.py OUTPUT_DIR

For every reference png (ie DO7.png) the png with the same name in
OUTPUT_DIR (made by fancychords -c from reference_chords.txt) must look
the same. Exit status 1 if one is missing or different.

PNG files made on different computers are never byte-identical: the
anti-aliasing of the text edges depends on the Cairo and FreeType
versions (about 1% of the pixels change by a few levels). So an image
passes when less than 0.5% of its pixels differ by more than 64/255.
A missing font is caught: the text is drawn with another font and about
3-4% of the pixels change completely.
"""

# standard library imports
import os
import sys

# third party imports (Pillow is installed with cairosvg)
from PIL import Image, ImageChops

# max share of pixels allowed to differ by more than DIFF_LEVEL
MAX_DIFF_SHARE = 0.005
DIFF_LEVEL = 64


def compare(reference_png, output_png):
    '''
    return (ok, message) for one couple of images
    '''
    if not os.path.isfile(output_png):
        return False, 'missing ' + output_png
    ref = Image.open(reference_png).convert('RGBA')
    out = Image.open(output_png).convert('RGBA')
    if ref.size != out.size:
        return False, 'size %s instead of %s' % (out.size, ref.size)
    # max difference over the 4 channels, for every pixel
    diffs = [max(px) for px in ImageChops.difference(ref, out).get_flattened_data()]
    share = sum(1 for d in diffs if d > DIFF_LEVEL) / len(diffs)
    message = '%.2f%% of the pixels differ by more than %d/255' % (100 * share, DIFF_LEVEL)
    return share <= MAX_DIFF_SHARE, message


if __name__ == '__main__':
    output_dir = sys.argv[1]
    reference_dir = os.path.dirname(os.path.abspath(__file__))
    all_ok = True
    for name in sorted(f for f in os.listdir(reference_dir) if f.endswith('.png')):
        ok, message = compare(os.path.join(reference_dir, name), os.path.join(output_dir, name))
        print(('OK    ' if ok else 'FAIL  ') + name + ': ' + message)
        all_ok = all_ok and ok
    sys.exit(0 if all_ok else 1)
