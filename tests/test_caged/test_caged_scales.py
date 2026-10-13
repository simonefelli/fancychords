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
    from libs import scale_parser
    from libs import htmlreport
    from libs import scales2files
    
    # --- internal parameters ---
    sd = 55.00                      # string distance, optimal ratio is fd/sd = 1.30 - 1.40
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings, is 6 for guitar
    nf = 4                          # number of frets, should be no more than 4 for chords
    debug = False                   # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.40                  # fret distance                                
    radius_factor = 22.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples

    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    
    # --- functions parameters ---
    input_way = 'file'                      # what input_crds represent, can be either 'string' or 'file'
    horiz = True                            # if true scale is horizontal otherwise vertical
    enable_dotlabels = True                 # if True enable dot labels
    enable_footer = True                   # if True enable footer labels
    convert_flag = True                     # if true output also png file     
    font_weight = 'normal'                  # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono derivative FChords'             # global font family: ['Courier New' | 'Ubuntu Mono' | 
                                            # 'DejaVu Sans Mono' | 'Liberation Mono']
    # --- appearance  parameters
    scale_label_font_weight = None          # main scale label, font weight
    scale_label_font_family = None          # main scale label, font family
    scale_label_font_factor = None          # main scale label, font size factor: default is 0.50
    upper_labels_font_weight = None         # upper labels, font weight
    upper_labels_font_family = None         # upper labels, font family   
    upper_labels_font_factor = None         # upper labels, font size factor: default is 1.15
    bottom_labels_font_weight = None        # bottom labels, font weight
    bottom_labels_font_family = None        # bottom labels, font family      
    bottom_labels_font_factor = None         # bottom labels, font size factor: default is 0.80
    side_labels_font_weight = None          # side labels, font weight
    side_labels_font_family = None          # side labels, font family
    side_labels_font_factor = None          # side labels, font size factor  : default is 0.70

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
          '*': (1.0, 'black', '1.0', 
                'black', '1.0', 'none', fair_stroke_str, 
                'white', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'r': (0.9, 'lightgrey', '1.0', 
                'black', '1.0', 'none', fat_stroke_str, 
                'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                True, False)
        , 'b3':(1.0, 'lightsalmon', '1.0', 
                'black', '1.0', 'none', fair_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'b5':(1.0, 'skyblue', '1.0', 
                'black', '1.0', 'none', fair_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'b7': (1.0, 'lightgreen', '1.0', 
                'black', '1.0', 'none', fair_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
    }
    
    fret0_format = {
          '*': (1.05, 'black', '0.7', 
                'black', '0.0', 'dashes', fair_stroke_str, 
                'white', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'r': (0.9, 'lightgrey', '0.7', 
                'black', '1.0', 'dashes', fair_stroke_str, 
                'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                True, False)
        , 'b3': (1.0, 'lightsalmon', '0.7', 
                 'black', '1.0', 'dashes', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                 False, False)
        , 'b5': (1.0, 'skyblue', '0.7', 
                 'black', '1.0', 'dashes', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                 False, False)
        , 'b7':  (1.0, 'lightgreen', '0.7', 
                 'black', '1.0', 'dashes', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                 False, False)
    }

    # arrows_format default
    # -------------------------
    # (
    #   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
    #  )
    arrows_format = (lntk, 'black', '1.0', 'e', True, '')
    
    
    # ------ caged scales  ------
    
    ncols = 2                               # number of columns for the gallery
    thumb_width = '300.0px'                 # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    input_scalesfile = '../scls_tests_files/caged_scales.txt' # path for scale list txt      
    dir_output = './dirout/scales/forms'    # output dir for images
    fret0 = False                     # if True you can draw dots above nut 
    enable_header = False             # if True enable header labels
    nutline = False                   # if True draw nut line ticker
    enable_fretnum = True             # if true enable side labels
    scale_label_isbottom = True       # if true scale main label goes at the bottom
    scale_label_isleft = True         # if true scale main label is left aligned otherwise is centered
    padding = None                    # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable


    # ------ useful message (input scales details)  ------

    return_scl_list_from_file = scale_parser.get_scales_list_from_file(input_scalesfile, print_output=False)[0]
    print('\nscl_list_from_file (' + str(len(return_scl_list_from_file)) + \
          ' scales):\n===============================')
    for elem in return_scl_list_from_file:
        scale_name = elem[2]
        root_note = elem[1]
        frets = elem[5]
        interv = elem[6]         
        print('{:<10} {}'.format(scale_name, str(frets)))
        print('{:<10} {}'.format('', str(interv)))

    # --------------------------------------------------

    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = scales2files.process_scales_file(
            input_scalesfile, 
            dir_output, horiz, enable_header, enable_dotlabels, 
            enable_footer, enable_fretnum, nutline, 
            fret0, font_weight, font_family,
            scale_label_font_weight, scale_label_font_family, 
            scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
            fretb_format, fret0_format, arrows_format, padding, 
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, 
            convert_flag, debug
        )

    if report != 'disable':
        file_exts = ('.svg', '.png')
        process_scales_msg_str += '\n' + htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)


    # ------ complete all neck scale  ------

    ncols = 1                                   # number of columns for the gallery
    thumb_width = '1100.0px'                    # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    input_scalesfile = '../scls_tests_files/scales-all-neck.txt'  # path for scale list txt
    dir_output = './dirout/scales/complete'     # output dir for images
    fret0 = True                      # if True you can draw dots above nut
    enable_header = True              # if True enable header labels 
    nutline = True                    # if True draw nut line ticker
    enable_fretnum = True             # if true enable side labels
    scale_label_isbottom = False      # if true scale main label goes at the bottom
    scale_label_isleft = False        # if true scale main label is left aligned otherwise is centered
    padding = None                    # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable


    # ------ useful message (input scales details)  ------

    return_scl_list_from_file = scale_parser.get_scales_list_from_file(input_scalesfile, print_output=False)[0]
    print('\nscl_list_from_file (' + str(len(return_scl_list_from_file)) + \
          ' scales):\n===============================')
    for elem in return_scl_list_from_file:
        scale_name = elem[2]
        root_note = elem[1]
        frets = elem[5]
        interv = elem[6]         
        print('{:<10} {}'.format(scale_name, str(frets)))
        print('{:<10} {}'.format('', str(interv)))

    # --------------------------------------------------

    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = scales2files.process_scales_file(
            input_scalesfile, 
            dir_output, horiz, enable_header, enable_dotlabels, 
            enable_footer, enable_fretnum, nutline, 
            fret0, font_weight, font_family,
            scale_label_font_weight, scale_label_font_family, 
            scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
            fretb_format, fret0_format, arrows_format, padding, 
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, 
            convert_flag, debug
        )

    if report != 'disable':
        file_exts = ('.svg', '.png')
        process_scales_msg_str += '\n' + htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)
    

    # ------ caged  padded scales  ------
    
    ncols = 1                               # number of columns for the gallery
    thumb_width = '1100.0px'                 # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    input_scalesfile = '../scls_tests_files/caged_scales.txt' # path for scale list txt      
    dir_output = './dirout/scales/forms_pad'    # output dir for images
    fret0 = False                     # if True you can draw dots above nut 
    enable_header = False             # if True enable header labels
    nutline = True                   # if True draw nut line ticker
    enable_fretnum = True             # if true enable side labels
    scale_label_isbottom = False       # if true scale main label goes at the bottom
    scale_label_isleft = True         # if true scale main label is left aligned otherwise is centered
    padding = (0, 16)                 # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable


    # ------ useful message (input scales details)  ------

    return_scl_list_from_file = scale_parser.get_scales_list_from_file(input_scalesfile, print_output=False)[0]
    print('\nscl_list_from_file (' + str(len(return_scl_list_from_file)) + \
          ' scales):\n===============================')
    for elem in return_scl_list_from_file:
        scale_name = elem[2]
        root_note = elem[1]
        frets = elem[5]
        interv = elem[6]         
        print('{:<10} {}'.format(scale_name, str(frets)))
        print('{:<10} {}'.format('', str(interv)))

    # --------------------------------------------------

    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = scales2files.process_scales_file(
            input_scalesfile, 
            dir_output, horiz, enable_header, enable_dotlabels, 
            enable_footer, enable_fretnum, nutline, 
            fret0, font_weight, font_family,
            scale_label_font_weight, scale_label_font_family, 
            scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
            fretb_format, fret0_format, arrows_format, padding, 
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, 
            convert_flag, debug
        )

    if report != 'disable':
        file_exts = ('.svg', '.png')
        process_scales_msg_str += '\n' + htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)