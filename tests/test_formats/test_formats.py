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

import os
import svgwrite
from libs import draw_dots
from libs import convert_svg2png


# full path for chord image svg file
crd_file = './test_formats.svg'

ns = 6         # number of strings
nf = 4         # number of frets
radius = 25.0  # dot radius, radius = sd * radius_factor

# circle dot_stroke_dasharray = (radius * dot_radius_scale) / 3.816
# rect   dot_stroke_dasharray = (radius * dot_radius_scale) / 3.993

# draw_dots tuples formats:
# -------------------------
# (
#   dot_radius_scale, dot_fill, dot_fill_opacity, 
#   dot_stroke, dot_stroke_opacity, dot_stroke_dasharray, dot_stroke_width, 
#   label_fill, label_fill_opacity, dot_labelfont_weight, dot_labelfont_family, 
#   dot_isquare, dot_rotate
#  )

fretb_format = {
      '*': (1.0, 'black', '1.0', 
            'black', '1.0', 'none', '3.5', 
            'white', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
            False, False)
    , 'r': (0.9, 'lightgrey', '1.0', 
            'black', '1.0', 'none', '5', 
            'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
            True, False)
    , 'rh': (0.9, 'white', '1.0', 
             'grey', '1.0', 'dashes', '3.5', 
             'grey', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
             True, False)
    , '3': (1.0, 'lightsalmon', '1.0', 
            'black', '1.0', 'none', '5', 
            'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
            False, False)
    , '3h': (1.0, 'white', '1.0', 
             'grey', '1.0', 'dashes', '3.5', 
             'grey', '1.0', 'bold', 'Ubuntu Mono derivative FChords',
              False, False)
    , '5': (1.0, 'skyblue', '1.0', 
            'black', '1.0', 'none', '5', 
            'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
            False, False) 
    , 'b5': (1.0, 'skyblue', '1.0', 
            'black', '0.3', 'none', '5', 
            'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
            False, False)
    , '6': (1.0, 'yellow', '1.0', 
            'black', '1.0', 'none', '5', 
            'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
            False, False) 
    , 'b6': (1.0, 'yellow', '1.0', 
            'black', '1.0', 'none', '5', 
            'black', '0.3', 'normal', 'Ubuntu Mono derivative FChords', 
            False, False) 
    , '7': (1.0, 'lightgreen', '1.0', 
             'black', '1.0', 'none', '5', 
             'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
    , 'b7': (1.0, 'lightgreen', '0.3', 
             'black', '1.0', 'none', '5', 
             'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
    , '9': (1.0, 'violet', '1.0', 
             'black', '1.0', 'none', '5', 
             'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
    , 'b9': (1.0, 'violet', '0.3', 
             'black', '0.3', 'none', '5', 
             'black', '0.3', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
}

fret0_format = {
      '*': (1.0, 'white', '1.0', 
            'black', '1.0', 'dashes', '3.5', 
            'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
            False, False)
    , 'r': (1.0, 'lightgrey', '1.0', 
            'black', '1.0', 'dashes', '3.5', 
            'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
            True, False)
}

centers_matrix = [
    [(50.0,  50), (150.0,  50), (250.0,  50), (350.0,  50), (450.0,  50)], 
    [(50.0, 150), (150.0, 150), (250.0, 150), (350.0, 150), (450.0, 150)], 
    [(50.0, 250), (150.0, 250), (250.0, 250), (350.0, 250), (450.0, 250)], 
    [(50.0, 350), (150.0, 350), (250.0, 350), (350.0, 350), (450.0, 350)], 
    [(50.0, 450), (150.0, 450), (250.0, 450), (350.0, 450), (450.0, 450)]
]

dwg = svgwrite.Drawing(filename=crd_file, size=(500 , 500), debug=True)

"""
mynote(dot, radius, interval, label, fret0, centers_matrix,
    fretb_format, fret0_format,
    dwg, ns
    )
"""

draw_dots.mynote(
                    (0, 6), radius, 'R', 'R', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (1, 6), radius, 'R', 'R', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (2, 6), radius, 'Rh', 'R', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (3, 6), radius, 'Rh', 'R', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (4, 6), radius, 'Rh', 'R', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
#=================

draw_dots.mynote(
                    (0, 5), radius, '4', '4', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (1, 5), radius, '3', '3', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (2, 5), radius, '3h', '3', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (3, 5), radius, '2', '2', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (4, 5), radius, '2', '2', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )

#=================

draw_dots.mynote(
                    (1, 4), radius, '5', '5', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (2, 4), radius, 'b5', 'b5', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (3, 4), radius, '7', '7', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (4, 4), radius, 'b7', 'b7', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )

#=================

draw_dots.mynote(
                    (1, 3), radius, '6', '6', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (2, 3), radius, 'b6', 'b6', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (3, 3), radius, '9', '9', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )
draw_dots.mynote(
                    (4, 3), radius, 'b9', 'b9', True, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )

#=================

dwg.save()

# './test_formats.svg' -> 'test_formats.svg'
actual_fullfilename = os.path.basename(crd_file)
# 'test_formats.svg' -> ('test_formats', '.svg')
actual_filename = os.path.splitext(actual_fullfilename)
msg_str, png_file_path_list = convert_svg2png.convert_svg2png('./', './', [actual_filename[0]])