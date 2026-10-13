# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Simone Felli
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
import_tvk_json: read chords from a tvk json file (a dict
{chord_name: [{'positions': [...], 'fingerings': [[...]]}, ...]}) and turn
them into chord lists for chord_parser.get_crd_list_from_str_list().
"""


# standard library imports
import os
import json

# local application imports
from libs import chord_parser


def parse_tvk_chord_name(chord_name):
    '''
    given a tvk chord name return root_note, quality, details
    '''
    (note, quality, detail, slash_note) = chord_parser.parse_chord_name(chord_name)
    return (chord_name, note, quality, detail, slash_note)


def study_tvk_json_chords(infile):
    '''
    not used just to group chord qualities
    '''
    crdnames_list = []
    crdqual_dict = {}    
    with open(infile, mode='r', encoding='utf-8') as infile:
        # data is a dict {chord_name:[...]}
        data = json.load(infile)
        chord_name, note, quality, detail = '', '', '', ''
        for chord_name in data:
            chord_name, note, quality, detail, slash_note = parse_tvk_chord_name(chord_name)
            #dirout = os.path.join(note, quality)
            crdnames_list.append((chord_name, note, quality, detail, slash_note))
            if quality in crdqual_dict:
                crdqual_dict[quality] += 1
            else:
                crdqual_dict[quality] = 1
        sort_crdqual = sorted(list(crdqual_dict.items()), key=lambda x: x[1], reverse=True)
    return crdnames_list, sort_crdqual


def parse_tvk_json_file(input_jsonf):
    '''
    given a tvk chord file return crd_list compatible with
    chord_parser.get_crd_list_from_str_list like
    [ chord_name, 'frets', 'fingers', 'dlabels', 'footer', 'subfolder' ]
    [ [ chord_name, 'frets', 'fingers', 'dlabels', 'footer', 'subfolder' ], ... ]
    ie (only chord_name and frets are mandatory):
        [['C', 'x,3,2,0,1,0', 'x,3,2,x,1,x'], ['C/C#', 'x,4,5,5,5,x', 'x,1,2,3,4,x'], ...]
    
    input_jsonf: String, input tvk json in style
    
    return tuple (msg_str, crd_list)   (note the order: message first)
    where crd_list is 
    [
        [chord_name, frets, fingers, intervals, dlabels, footer, subfolder]
        , ...
    ]
    with '%' for intervals, dlabels and footer and 'note/quality' as subfolder
    '''
    crd_list = []
    msg_str = ''   
    with open(input_jsonf, mode='r', encoding='utf-8') as input_jsonf:
        # data is a dict {chord_name:[...]}
        data = json.load(input_jsonf)
        for chord_name, chord_forms in list(data.items()):
            # exclude [null] forms
            chord_forms = [elem for elem in chord_forms if elem]
            # parse_tvk_chord_name() -> chord_name, note, quality, details
            tvk_chord_name = parse_tvk_chord_name(chord_name)
            chord_name = tvk_chord_name[0]
            note = tvk_chord_name[1]
            quality = tvk_chord_name[2]
            dirout = os.path.join(note, quality)
            my_row = '\n' + '-' * 42 + '\n'
            msg_str += my_row + '\nChord: ' + chord_name + '\n' * 2
            for form in chord_forms:
                # reset for every form: a form without 'positions' or
                # 'fingerings' must not reuse the values of the previous one
                frets, fingers = '', '%'
                for fret_fing_str, fret_fing_lst in list(form.items()):
                    if fret_fing_str == 'positions':
                        frets = ",".join([el for el in fret_fing_lst])
                        msg_str += 'pos: ' + frets + '\t'
                    elif fret_fing_str == 'fingerings' and fret_fing_lst:
                        # only the first fingering is used, '0' (no finger) -> 'x'
                        fing_lst = [el for el in fret_fing_lst[0]]
                        fing_lst_fltrd = [el if el != '0' else 'x' for el in fing_lst]
                        fingers = ",".join(fing_lst_fltrd)
                        msg_str += 'fing: ' + fingers + '\n'
                crd_list.append([chord_name, frets, fingers, '%', '%', '%', dirout])
        msg_str += my_row
    return (msg_str , crd_list)



if __name__ == "__main__":
    
    # testing local application imports
    from libs import chords2files
    from libs import htmlreport

    # --- internal parameters ---
    sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings, is 6 for guitar
    nf = 4                          # number of frets, should be no more than 4 for chords
    debug = False                    # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.30                  # fret distance                                
    radius_factor = 20.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples
    barre_strk_wdth = 1.10 * lntk   # barre arc tickness
    
    # --- html report parameters
    ncols = 4               # number of columns for the gallery
    thumb_width = '200.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

    # --- functions parameters ---
    input_jsonf = '../tests/misc_tests_files/tvk_small.json'       # full path for tvk json chord file
    dir_output = '../dirout'                # output dir for images
    horiz = False                           # if true chord is horizontal otherwise vertical
    chord_label_isbottom = False            # if true chord main label goes at the bottom
    chord_label_isleft = False              # if true chord main label is left aligned otherwise is centered
    enable_header = True                    # if True enable header labels
    enable_dotlabels = True                 # if True enable dot labels
    enable_footer = True                    # if True enable footer labels
    enable_barre = True                     # if true draw barre/s on chord
    enable_fretnum = True                   # if true enable side labels
    nutline = True                          # if True draw nut line ticker
    fret0 = False                           # if True you can draw dots above nut
    convert_flag = False                    # if true output also png file
    font_weight = 'bold'                    # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Courier New'        # global font family: ['Courier New' | 'Ubuntu Mono' | 
                                            # 'DejaVu Sans Mono' | 'Liberation Mono']
    chord_label_font_weight = None          # main chord label, font weight
    chord_label_font_family = None          # main chord label, font family 
    chord_label_font_factor = None          # main chord label, font size factor: default is 0.70
    upper_labels_font_weight = None         # upper labels, font weight
    upper_labels_font_family = None         # upper labels, font family   
    upper_labels_font_factor = None         # upper labels, font size factor: default is 1.15
    bottom_labels_font_weight = None        # bottom labels, font weight
    bottom_labels_font_family = None        # bottom labels, font family      
    bottom_labels_font_factor = None        # bottom labels, font size factor: default is 1.00
    side_labels_font_weight = None          # side labels, font weight
    side_labels_font_family = None          # side labels, font family
    side_labels_font_factor = None          # side labels, font size factor  : default is 0.90

                         
    # calculate fretx_format dot_stroke_width from lntk
    slim_stroke_str = str(lntk * 1.00)
    fat_stroke_str =  str(lntk * 1.66)

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
                'black', '1.0', 'none', slim_stroke_str, 
                'white', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'none', fat_stroke_str,
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
    }



    file_exts = ('.svg', '.png')
    
    crdnames_list, sort_crdqual = study_tvk_json_chords(input_jsonf)
    print('Testing study_tvk_json_chords')
    for elem in sort_crdqual:
        print(elem[0])
    
    
    msg_str, crd_list = parse_tvk_json_file(input_jsonf)
    
    for elem in crd_list: print(elem)
    # print msg_str
    
    final_crd_list, msg_str = chord_parser.get_crd_list_from_str_list(crd_list)
    
    for elem in final_crd_list: print(elem)
    
    chord_list_to_files = chords2files.chord_list_to_files(
        final_crd_list, 
        dir_output, horiz,enable_header, enable_dotlabels, 
        enable_footer, enable_barre, enable_fretnum,
        barre_strk_wdth, nutline, fret0, 
        font_weight, font_family,
        chord_label_font_weight, chord_label_font_family,
        
        chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
        
        fretb_format, fret0_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, 
        convert_flag, debug
        )

    htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)
    