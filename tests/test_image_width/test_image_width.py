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


# third party imports

import os
from libs import draw_chords


# --- internal parameters ---
sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
                                # image_w = (6.30*sd) + 43.0
                                # image_h = (9.79*sd) + 43.0
lntk = 3.00                     # grid line tickness
x_or = 20.00                    # fretboard box origin offset (x)
y_or = 20.00                    # fretboard box origin offset (y)
ns = 6                          # number of strings, is 6 for guitar
nf = 4                          # number of frets, should be no more than 4 for chords
debug = True                    # if true draw debug borders and debug dots
#  --- derived internal parameters ---
fd = sd * 1.30                  # fret distance                                
radius_factor = 20.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                # as a guideline: radius_factor = (20.00/sd)
                                # general formula for radius is: radius = sd * radius_factor
                                # single dot adjustments can be achieved through dot_radius_scale
                                # in fretx_format tuples
barre_strk_wdth = 1.10 * lntk   # barre arc tickness


# --- functions parameters ---
dir_output = './dirout'               # output dir for chord image
horiz = False                       # if true chord is horizontal otherwise vertical
chord_label_isbottom = False         # if true chord main label goes at the bottom
chord_label_isleft = False          # if true chord main label is left aligned otherwise is centered
enable_header = True                # if True enable header labels
enable_dotlabels = True             # if True enable dot labels
enable_footer = True                # if True enable footer labels
enable_barre = True                 # if true draw barre/s on chord
enable_fretnum = True               # if true enable side labels
nutline = True                      # if True draw nut line ticker
fret0 = False                       # if True you can draw dots above nut

font_weight = 'normal'              # global font weight: [ 'normal' | 'bold' ]
font_family = 'Ubuntu Mono Legacy'         # global font family: ['Courier New' | 'Ubuntu Mono' | 
                                    # 'DejaVu Sans Mono' | 'Liberation Mono']
fret0_format = {}                   # fret0_format, for fret0 dots
fretb_format = {}                   # fretb_format, for fretboard dots

chord_label_font_weight = None      # main chord label, font weight
chord_label_font_family = None      # main chord label, font family
chord_label_font_factor = None      # main chord label, font size factor: default is 0.70
upper_labels_font_weight = None     # upper labels, font weight
upper_labels_font_family = None     # upper labels, font family   
upper_labels_font_factor = None     # upper labels, font size factor: default is 1.15
bottom_labels_font_weight = None    # bottom labels, font weight
bottom_labels_font_family = None    # bottom labels, font family      
bottom_labels_font_factor = None    # bottom labels, font size factor: default is 1.00
side_labels_font_weight = None      # side labels, font weight
side_labels_font_family = None      # side labels, font family
side_labels_font_factor = None      # side labels, font size factor  : default is 0.90



def smartargs(chordname, fd, sd, dir_output, args):
    (horiz, enable_header, enable_dotlabels,
    enable_footer, enable_barre, enable_fretnum,
    barre_strk_wdth, nutline, fret0, font_weight, font_family,
    chord_label_font_weight, chord_label_font_family, 
    chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
    fretb_format, fret0_format,
    upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
    bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
    side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
    lntk, x_or, y_or, ns, nf, radius_factor, debug
     ) = args
    
    if dir_output:
        # if dir_output does not exist then create it
        dir_output += '/'
        if not os.path.isdir(dir_output): os.makedirs(dir_output)
        return (
            chordname, chordname,
            ['x', '4', '6', '6', '6', '8'], ['x', '1', '3', '3', '3', '4'], ['x', 'R', '5', 'b7', 'b3', '5'], 
            ['x', 'R', '5', 'm7', 'm3', '5'], ['x', '1', '3', '3', '3', '4'],
            dir_output, horiz, enable_header, enable_dotlabels,
            enable_footer, enable_barre, enable_fretnum,
            barre_strk_wdth, nutline, fret0, font_weight, font_family,
            chord_label_font_weight, chord_label_font_family, 
            chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
            fretb_format, fret0_format,
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
            )
    else:
        return (
            chordname,
            ['x', '4', '6', '6', '6', '8'], ['x', '1', '3', '3', '3', '4'], ['x', 'R', '5', 'b7', 'b3', '5'], 
            ['x', 'R', '5', 'm7', 'm3', '5'], ['x', '1', '3', '3', '3', '4'],
            horiz, enable_header, enable_dotlabels,
            enable_footer, enable_barre, enable_fretnum,
            barre_strk_wdth, nutline, fret0, font_weight, font_family,
            chord_label_font_weight, chord_label_font_family, 
            chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
            fretb_format, fret0_format,
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
            )


args = (
     horiz, enable_header, enable_dotlabels,
     enable_footer, enable_barre, enable_fretnum,
     barre_strk_wdth, nutline, fret0, font_weight, font_family,
     chord_label_font_weight, chord_label_font_family, 
     chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
     fretb_format, fret0_format, 
     upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
     bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
     side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
     lntk, x_or, y_or, ns, nf, radius_factor, debug
    )


print('sd', '\timage_w', '\timage_h', '\n================================')
for sd in range (30, 100, 1):
    chordname = 'cn_' + "{:03d}".format(sd)
    sd = sd * 1.00
    fd = sd * 1.30
    (
          dwg, (x0, y0)
        , (ftbrd_w, ftbrd_h)
        , (ftbrd_box_w, ftbrd_box_h)
        , (image_w, image_h)
    ) = draw_chords.draw_chord(
        *smartargs(chordname, fd, sd, None, args)
        )
    print(sd, '\t', round(image_w, 3), '\t', round(image_h, 3))
    draw_chords.chord_to_file(
        *smartargs(chordname, fd, sd, dir_output, args)
        )
    
from libs import htmlreport
file_exts = (".svg",)
htmlreport.generate_htmlreport(dir_output, file_exts, 4, None)


# Regression (in libreoffice, Data -> Statistic -> Regression) says:
# image_w = (6.30*sd) + 43.0
# image_h = (9.79*sd) + 43.0
