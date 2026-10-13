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



if __name__ == "__main__":
    
    # testing this function
    
    # --- functions parameters ---

    # local application imports
    from libs import chord_parser
    from libs import chords2files
    from libs import htmlreport
    
    # --- internal parameters ---
    sd = 55.00                      # string distance, optimal ratio is fd/sd = 1.30
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings, is 6 for guitar
    nf = 4                          # number of frets, should be no more than 4 for chords
    debug = False                    # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.40                  # fret distance                                
    radius_factor = 22.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples
    barre_strk_wdth = 1.10 * lntk   # barre arc tickness

    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    ncols = 6               # number of columns for the gallery
    thumb_width = '300.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    
    # --- functions parameters ---
    input_way = 'file'                      # what input_crds represent, can be either 'string' or 'file'
    input_crdf = '../crds_test_files/caged_chords.txt'       # path for chord list txt
    dir_output = './dirout/chords'          # output dir for images
    horiz = False                           # if true chord is horizontal otherwise vertical
    chord_label_isbottom = False            # if true chord main label goes at the bottom
    chord_label_isleft = False              # if true chord main label is left aligned otherwise is centered
    enable_header = True                    # if True enable header labels
    enable_dotlabels = True                 # if True enable dot labels
    enable_footer = True                    # if True enable footer labels
    enable_barre = True                     # if true draw barre/s on chord
    enable_fretnum = False                  # if true enable side labels
    nutline = False                         # if True draw nut line ticker
    convert_flag = True                     # if true output also png file    
    fret0 = True                            # if True you can draw dots above nut  
    font_weight = 'normal'                  # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono Legacy'             # global font family: ['Courier New' | 'Ubuntu Mono' | 
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
    fair_stroke_str = str(lntk * 1.16)
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
          '*':  (1.0, 'black', '1.0', 
                 'black', '1.0', 'none', slim_stroke_str, 
                 'white', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'rh': (0.9, 'white', '1.0', 
                 'grey', '1.0', 'dashes', fair_stroke_str, 
                 'grey', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 True, False)
        , 'r':  (0.9, 'lightgrey', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 True, False)
        , '3':  (1.0, 'lightsalmon', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
        , 'b3': (1.0, 'lightsalmon', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , '5h': (1.0, 'white', '1.0', 
                 'grey', '1.0', 'dashes', fair_stroke_str, 
                 'grey', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'b7': (1.0, 'lightgreen', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , '7':  (1.0, 'lightgreen', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', fair_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (0.9, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', fair_stroke_str, 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                True, False)
    }


    # ------ useful message (input chords details)  ------

    return_crd_list_from_file = chord_parser.get_crd_list_from_file(input_crdf, print_output=False)[0]
    print('\ncrd_list_from_file (' + str(len(return_crd_list_from_file)) + \
          ' chords):\n===============================')
    for elem in return_crd_list_from_file:
        chord_name = elem[0]
        root_note = elem[1]
        frets = elem[3]
        fingers = elem[4]
        interv = elem[6]       
        print('{:<15} {:<35} {}'.format(chord_name, str(frets), str(interv)))

    # --------------------------------------------------


    # check if report has to be done
    if report != 'only':
        (  process_chords_msg_str
         , svg_file_path_list
         , png_file_path_list) = chords2files.process_chords(
           input_crdf, input_way,
           dir_output, horiz, enable_header, enable_dotlabels, 
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
    if report != 'disable':
        file_exts = ('.svg', '.png')
        htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)