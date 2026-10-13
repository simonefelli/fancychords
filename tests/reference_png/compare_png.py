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
Compare png chord images, to check the font used by fancychords.

    python compare_png.py OUTPUT_DIR
        every reference png of this folder (ie DO7.png) and the png with the
        same name in OUTPUT_DIR (made by fancychords -c from
        reference_chords.txt) must look the same

    python compare_png.py --same DIR1 DIR2
        the png files with the same name in the 2 dirs must be identical,
        pixel by pixel (images made on the same computer)

    python compare_png.py --differ DIR1 DIR2
        the png files with the same name in the 2 dirs must be different

Exit status 1 if a check fails.

The first check compares with images made on Simone's computer. PNG files
made on different computers are never byte-identical: the anti-aliasing
of the text edges depends on the Cairo and FreeType versions. With the
right font up to about 0.5% of the pixels differ by more than 64/255
(seen on Ubuntu 22.04), with a missing font 3-4%: an image passes below
1.5%. This works only on Linux: Windows draws text with its own font
system, so its images differ more from Linux ones.

The --same / --differ checks work everywhere (images drawn on the same
computer): chords drawn with the default font 'Ubuntu Mono derivative
FChords' must be different from chords drawn with a font that does not
exist (the font is really installed and used), and must not change when
other fonts are installed too (ie the newer Ubuntu Mono of Ubuntu 24.04).
"""

# standard library imports
import os
import sys

# third party imports (Pillow is installed with cairosvg)
from PIL import Image, ImageChops

# max share of pixels allowed to differ by more than DIFF_LEVEL
MAX_DIFF_SHARE = 0.015
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


def pixels_equal(png1, png2):
    '''
    True if the 2 images have the same size and the same pixels
    '''
    img1 = Image.open(png1).convert('RGBA')
    img2 = Image.open(png2).convert('RGBA')
    return img1.size == img2.size and ImageChops.difference(img1, img2).getbbox() is None


def compare_dirs(dir1, dir2, want_equal):
    '''
    compare the png files with the same name in dir1 and dir2: they must be
    all identical (want_equal True) or all different. Return True if so
    '''
    names = sorted(f for f in os.listdir(dir1) if f.endswith('.png'))
    if not names:
        print('FAIL  no png files in ' + dir1)
        return False
    all_ok = True
    for name in names:
        other = os.path.join(dir2, name)
        if not os.path.isfile(other):
            print('FAIL  missing ' + other)
            all_ok = False
            continue
        equal = pixels_equal(os.path.join(dir1, name), other)
        ok = (equal == want_equal)
        print(('OK    ' if ok else 'FAIL  ') + name + (': identical' if equal else ': different'))
        all_ok = all_ok and ok
    return all_ok


if __name__ == '__main__':
    if sys.argv[1] in ('--same', '--differ'):
        sys.exit(0 if compare_dirs(sys.argv[2], sys.argv[3], sys.argv[1] == '--same') else 1)
    output_dir = sys.argv[1]
    reference_dir = os.path.dirname(os.path.abspath(__file__))
    all_ok = True
    for name in sorted(f for f in os.listdir(reference_dir) if f.endswith('.png')):
        ok, message = compare(os.path.join(reference_dir, name), os.path.join(output_dir, name))
        print(('OK    ' if ok else 'FAIL  ') + name + ': ' + message)
        all_ok = all_ok and ok
    sys.exit(0 if all_ok else 1)
