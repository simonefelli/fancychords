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
make_social_preview: build assets/social_preview.png (1280 x 640), the image
GitHub shows when a link to the repository is shared (Settings -> General ->
Social preview), from the example diagrams of the README.

The title is written with the FChords font of fonts/, and the diagrams are
rendered from the SVG files of assets/ at twice the size, then reduced, so
they stay sharp. Their labels need the FChords font installed (see fonts/).

    python3 assets/make_social_preview.py
"""

# standard library imports
import io
import os

# third party imports (Pillow is installed with cairosvg)
import cairosvg
from PIL import Image, ImageDraw, ImageFont


ASSETS = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ASSETS, '..', 'fonts', 'ubuntu-mono-derivative-fchords')
OUTPUT = os.path.join(ASSETS, 'social_preview.png')

WIDTH, HEIGHT = 1280, 640
MARGIN = 50                      # GitHub may crop the edges: keep them empty
BACKGROUND = 'white'
TEXT = (30, 30, 30)
SUBTEXT = (95, 95, 95)

TITLE = 'FancyChords'
TAGLINE = 'Guitar chord & scale diagrams from plain text'
FOOTER = 'SVG · PNG · CAGED · free and open source (GPL)'

# diagrams drawn from left to right, all with the same height
DIAGRAMS = ['C Major.v02.svg', 'C7.v02.svg', 'D Form.svg']
DIAGRAM_H = 360
GAP = 40


def render_svg(svg_name, height):
    '''
    render one svg of assets/ on a white background, height pixels high
    '''
    png = cairosvg.svg2png(url=os.path.join(ASSETS, svg_name), scale=2)
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    bg = Image.new('RGBA', im.size, BACKGROUND)
    bg.alpha_composite(im)
    width = round(im.width * height / im.height)
    return bg.convert('RGB').resize((width, height), Image.LANCZOS)


def main():
    canvas = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    bold = os.path.join(FONTS, 'UbuntuMonoderivativeFChords-B.ttf')
    regular = os.path.join(FONTS, 'UbuntuMonoderivativeFChords-R.ttf')

    # title and tagline, centered
    y = MARGIN - 10
    for text, font, color in ((TITLE, ImageFont.truetype(bold, 84), TEXT),
                              (TAGLINE, ImageFont.truetype(regular, 36), SUBTEXT)):
        w = draw.textlength(text, font=font)
        draw.text(((WIDTH - w) / 2, y), text, font=font, fill=color)
        y += font.size + 12

    # diagrams, centered in a row
    images = [render_svg(name, DIAGRAM_H) for name in DIAGRAMS]
    row_w = sum(im.width for im in images) + GAP * (len(images) - 1)
    assert row_w <= WIDTH - 2 * MARGIN, 'diagrams too wide: %d' % row_w
    x = (WIDTH - row_w) // 2
    y_row = HEIGHT - MARGIN - 40 - DIAGRAM_H
    for im in images:
        canvas.paste(im, (x, y_row))
        x += im.width + GAP

    # footer line
    font = ImageFont.truetype(regular, 26)
    w = draw.textlength(FOOTER, font=font)
    draw.text(((WIDTH - w) / 2, HEIGHT - MARGIN - 26), FOOTER, font=font, fill=SUBTEXT)

    canvas.save(OUTPUT, optimize=True)
    print(OUTPUT, canvas.size, '%d KB' % (os.path.getsize(OUTPUT) // 1024))


if __name__ == '__main__':
    main()
