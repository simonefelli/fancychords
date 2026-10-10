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


# third party imports
import svgwrite

# local application imports
from libs import global_utilities
from libs import draw_dots
from libs import draw_fretbrd
from libs import mylabels
from libs import mymultilabels
from libs import draw_barre


def draw_chord_box(
        frets, fingers, intervals, dlabels, footer, 
        radius, centers_matrix,
        upper_labels_centers_vector, bottom_labels_centers_vector,
        side_labels_centers_vector, horiz_lines_vertex, vertcl_lines_vertex,
        ftbrd_box_wh, dwg, nutline, fret0, enable_header, enable_dotlabels,
        enable_footer, enable_barre, enable_fretnum,
        barre_strk_wdth, horiz,
        fretb_format, fret0_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor
        , lntk
        , x_or
        , y_or
        , ns
        , nf
        , fd
        , edge_debug
        ):
    """
    Draw single chord image with dots, labels, barre, headers, footer
    and side labels (NO chord name main label)

    frets: List of strings, fret sequence
    fingers: List of strings, finger numbers list
    intervals: List of strings, interval sequence
    dlabels: List of strings, dot labels sequence
    footer: List of strings, footer sequence
    radius: Number, dot radius in chord image
    centers_matrix: List of list, dot centers matrix     
    upper_labels_centers_vector: List of tuples, 
            upper dots labels point centers vector    
    bottom_labels_centers_vector: List of tuples, 
            bottom dots labels point centers vector
    side_labels_centers_vector: List of tuples, 
            side dots labels point centers vector    
    horiz_lines_vertex: List of tuples of tuples, 
            list with horizontal lines vertexs couples
    vertcl_lines_vertex: List of tuples of tuples, 
            list with vertical lines vertexs couples    
    ftbrd_box_wh: Tuple of number, (fretboard box width, fretboard box height)
    dwg: Svgwrite object
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels
    barre_strk_wdth: Number, barre arc tickness
    horiz: Boolean, if true chord is horizontal otherwise vertical
    xxx_format: Dict,
             interval: String, apply format to this interval dot -> tuple (
             dot_radius_scale: Number, dot radius scale factor
             dot_fill: String, color inside dot
             dot_fill_opacity: String, Dot fill opacity value
             dot_stroke: String, dot stroke width
             dot_stroke_opacity: String, Dot stroke fill opacity value
             dot_stroke_dasharray: String, dot stroke pattern of dashes and gaps,
                                   'dashes' to enable and None to disable
             dot_stroke_width: String, dot stroke width
             label_fill: String, label color
             label_fill_opacity: String, label fill opacity value
             dot_labelfont_weight: String, label font weight
             dot_labelfont_family: String, label font family
             dot_isquare: Boolean, if true draw square
             dot_rotate: Boolean, if true rotate dot by 90 deg
         )
         dicts are:
             fretb_format, for fretboard dots (fret >= 1)
             fret0_format, for fret0 dots (fret = 0)
    upper_labels_font_weight: String, upper labels, font weight
    upper_labels_font_family: String, upper labels, font family 
    upper_labels_font_factor: Number, upper labels, font size factor 
    bottom_labels_font_weight: String, bottom labels, font weight
    bottom_labels_font_family: String, bottom labels, font family   
    bottom_labels_font_factor: Number, bottom labels, font size factor      
    side_labels_font_weight: String, side labels, font weight
    side_labels_font_family: String, side labels, font family 
    side_labels_font_factor: Number, side labels, font size factor  
    lntk: Number, grid line tickness          
    x_or: Number, fretboard box origin (x)
    y_or: Number, fretboard box origin(y)    
    ns: Number, number of strings, is 6 for guitar
    nf: Number, number of frets. Should be no more than 4 for chords
    fd: Number, fret distance (px)
    edge_debug: Boolean, if true draw debug borders and debug dots

    return nothing
    """
    (ftbrd_box_w, ftbrd_box_h) = ftbrd_box_wh
    # frets_int:   ['x','4','6','5','6','0'] -> [None, 4, 6, 5, 6, 0]
    # fingers_int: ['x','1','3','1','2','1'] -> [None, 1, 3, 1, 2, 1]
    # max fret - > 6, min fret - > 4
    # note min_fret is never 0, ie: [None, 3, 2, 0, 1, 0] -> max fret=3, min fret=1
    
    (max_fret, min_fret) = global_utilities.max_min_fret_slst(frets)
    frets_int = global_utilities.crd_slst2ilst(frets)
    fingers_int = global_utilities.crd_slst2ilst(fingers)
      
    # if max_fret <= 4 then draw nut
    if max_fret > nf:
        first_fret = min_fret       # if first_fret > 4 there is no reason to draw nut. 
                                    # Instead draw starting fret number, min_fret is never 0
                                    # beacause of max_min_fret_slst() function
        nut = False                 # if nut is set to false do not draw nut on fretboard
        # put first fret as side labels
        side_labels = [str(min_fret), None, None]
    else:
        first_fret = 0          # if first_fret = 0 draw nut is allowed
        if nutline:             # but before check if nutline variable is True and after that  
            nut = True          # you can set nut to true to draw nut on fretboard
        else:
            nut = False
        # put '3' on third fret as side labels
        side_labels = [None, None, '3']
    
    # if header is present
    if enable_header:
        # if you draw dots above nut upper labels should be only of 'x'
        # upper header: ['x','3','2','0','1','0'] -> ['x',None,None,None,None,None]        
        if fret0:
            header = [fr if (not fr.isdigit()) else None for fr in frets]
        else:
        # if you do not draw dots above nut upper labels should be only of 'x' and '0'
        # upper header: ['x','3','2','0','1','0'] -> ['x',None,None,'0',None,'0']            
            header = [fr if ((not fr.isdigit()) or (fr.isdigit() and int(fr) == 0)) else None for fr in frets]
    else:
        # else do not draw header
        header = None
    # if enable_dotlabels is false do not draw dot labels
    if not enable_dotlabels: dlabels = []
    # if enable_footer is false do not draw footer
    if not enable_footer: footer = None   
    
    # draw fretboard
    draw_fretbrd.draw_fretbrd(nut, lntk, dwg,
                 horiz_lines_vertex,
                 vertcl_lines_vertex,
                 centers_matrix,
                 x_or, y_or,
                 ftbrd_box_w, ftbrd_box_h,
                 side_labels_centers_vector,
                 bottom_labels_centers_vector,
                 upper_labels_centers_vector,
                 enable_header=enable_header,
                 enable_footer=enable_footer,
                 edge_debug=edge_debug
                 )  

    # draw dots
    draw_dots.draw_dots(frets, intervals, dlabels, radius, fret0, first_fret, centers_matrix,
                        fretb_format, fret0_format,
                        dwg, ns)
    # draw upper labels
    mylabels.draw_labels(header, (radius * upper_labels_font_factor), 
                         upper_labels_centers_vector, dwg,
                         upper_labels_font_weight, upper_labels_font_family)
    # draw bottom labels
    mylabels.draw_labels(footer, (radius * bottom_labels_font_factor),
                         bottom_labels_centers_vector, dwg,
                         bottom_labels_font_weight, bottom_labels_font_family,
                         label_len_is_h=True)
    
    # if enable_fretnum then draw side labels
    if enable_fretnum:
        # if side frets number has two chars then use mylabel_given_hght instead
        # of mylabel_given_wdth (set label_len_is_h = True). Otherwise number it's too small
        if max([len(elem) for elem in side_labels if elem]) > 1:
            label_len_is_h = True
        else:
            label_len_is_h = False
        mylabels.draw_labels(side_labels, (radius * side_labels_font_factor), 
                             side_labels_centers_vector, dwg,
                             side_labels_font_weight, side_labels_font_family,
                             label_len_is_h=label_len_is_h)
    
    # draw barres
    draw_barre.draw_barre(enable_barre, frets_int, fingers_int, first_fret,
                          centers_matrix, nf, horiz, dwg, radius, fd, barre_strk_wdth)


def draw_chord(
        chord_name, frets, fingers, intervals, dlabels, footer,
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
        ):
    """
    draw a single chord, complete with chord name main label. Set also default formatting
    
    chord_name: String, chord name
    frets: List of strings, fret sequence
    fingers: List of strings, finger numbers list
    intervals: List of strings, interval sequence
    dlabels: List of strings, dot labels sequence
    footer: List of strings, footer sequence
    horiz: Boolean, if true chord is horizontal otherwise vertical
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels
    barre_strk_wdth: Number, barre arc tickness
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    font_weight: String, font weight
    font_family: String, font family
    chord_label_font_weight: String, Main chord label, font weight
    chord_label_font_family: String, Main chord label, font family
    chord_label_font_factor: Number, Main chord label, font size factor
    chord_label_isbottom: Boolean, if true chord main label goes at the bottom
    chord_label_isleft: Boolean, if true chord main label is left aligned otherwise is centered
    xxx_format: Dict,
             interval: String, apply format to this interval dot -> tuple (
             dot_radius_scale: Number, dot radius scale factor
             dot_fill: String, color inside dot
             dot_fill_opacity: String, Dot fill opacity value
             dot_stroke: String, dot stroke width
             dot_stroke_opacity: String, Dot stroke fill opacity value
             dot_stroke_dasharray: String, dot stroke pattern of dashes and gaps,
                                   'dashes' to enable and None to disable
             dot_stroke_width: String, dot stroke width
             label_fill: String, label color
             label_fill_opacity: String, label fill opacity value
             dot_labelfont_weight: String, label font weight
             dot_labelfont_family: String, label font family
             dot_isquare: Boolean, if true draw square
             dot_rotate: Boolean, if true rotate dot by 90 deg
         )
         dicts are:
             fretb_format, for fretboard dots (fret >= 1)
             fret0_format, for fret0 dots (fret = 0)
    upper_labels_font_weight: String, upper labels, font weight
    upper_labels_font_family: String, upper labels, font family 
    upper_labels_font_factor: Number, upper labels, font size factor 
    bottom_labels_font_weight: String, bottom labels, font weight
    bottom_labels_font_family: String, bottom labels, font family   
    bottom_labels_font_factor: Number, bottom labels, font size factor      
    side_labels_font_weight: String, side labels, font weight
    side_labels_font_family: String, side labels, font family 
    side_labels_font_factor: Number, side labels, font size factor 
    x_or: Number, fretboard box origin (x)
    y_or: Number, fretboard box origin(y)  
    lntk: Number, grid line tickness    
    ns: Number, number of strings, is 6 for guitar
    nf: Number, number of frets. Should be no more than 4 for chords
    fd: Number, fret distance (px)  
    sd: Number, string distance, optimal ratio is fd/sd = 1.2
    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41
    debug: Boolean, if true draw debug borders and debug dots

    return dwg object (needed) and 
        3 tuples (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h) just for debugging
    """

    # fretb_format and fret0_format default formats if note set. Moreover
    # if specific element (dot_label, chord_label, upper_labels) font_weight or font_family
    # are not set then default to global font_weight and font_family
    
    # draw_dots tuples formats:
    # -------------------------
    # (
    #   dot_radius_scale, dot_fill, dot_fill_opacity, 
    #   dot_stroke, dot_stroke_opacity, dot_stroke_dasharray, dot_stroke_width, 
    #   label_fill, label_fill_opacity, dot_labelfont_weight, dot_labelfont_family, 
    #   dot_isquare, dot_rotate
    #  )

    # calculate fretx_format dot_stroke_width from lntk
    slim_stroke_str = str(lntk * 1.00)
    fat_stroke_str =  str(lntk * 1.66)
    
    # fretb_format default
    if not fretb_format: fretb_format = {
          '*': (1.0, 'black', '1.0', 
                'black', '1.0', 'none', slim_stroke_str, 
                'white', '1.0', font_weight, font_family, 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'none', fat_stroke_str, 
                'black', '1.0', font_weight, font_family, 
                False, False)
        }
    
    # fretb_format default to global font_weight and font_family if not set
    if not fretb_format['*'][9]: 
        fretb_format['*'] = global_utilities.mytuplechange(fretb_format['*'], 9, font_weight)
    if not fretb_format['r'][9]: 
        fretb_format['r'] = global_utilities.mytuplechange(fretb_format['r'], 9, font_weight)
    if not fretb_format['*'][10]: 
        fretb_format['*'] = global_utilities.mytuplechange(fretb_format['*'], 10, font_family)
    if not fretb_format['r'][10]:
        fretb_format['r'] = global_utilities.mytuplechange(fretb_format['r'], 10, font_family)

    # fret0_format default
    if not fret0_format: fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', font_weight, font_family, 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', font_weight, font_family, 
                False, False)
        }
    
    # fret0_format default to global font_weight and font_family if not set
    if not fret0_format['*'][9]: 
        fret0_format['*'] = global_utilities.mytuplechange(fret0_format['*'], 9, font_weight)
    if not fret0_format['r'][9]: 
        fret0_format['r'] = global_utilities.mytuplechange(fret0_format['r'], 9, font_weight)
    if not fret0_format['*'][10]: 
        fret0_format['*'] = global_utilities.mytuplechange(fret0_format['*'], 10, font_family)
    if not fret0_format['r'][10]: 
        fret0_format['r'] = global_utilities.mytuplechange(fret0_format['r'], 10, font_family)

    # other font variables
    if not chord_label_font_weight: chord_label_font_weight = font_weight
    if not chord_label_font_family: chord_label_font_family = font_family
    if not chord_label_font_factor: chord_label_font_factor = 0.70
    if not upper_labels_font_weight: upper_labels_font_weight = font_weight
    if not upper_labels_font_family: upper_labels_font_family = font_family
    if not upper_labels_font_factor: upper_labels_font_factor = 1.15
    if not bottom_labels_font_weight: bottom_labels_font_weight = font_weight
    if not bottom_labels_font_family: bottom_labels_font_family = font_family
    if not bottom_labels_font_factor: bottom_labels_font_factor = 1.00
    if not side_labels_font_weight: side_labels_font_weight = font_weight
    if not side_labels_font_family: side_labels_font_family = font_family
    if not side_labels_font_factor: side_labels_font_factor = 0.90

    # check if fretboard number of frets are enough considering input frets list
    
    (max_fret, min_fret) = global_utilities.max_min_fret_slst(frets)
    
    delta_frets = max_fret - min_fret + 1
    # if not enough then set nf = delta_frets
    if (delta_frets) > nf: nf = delta_frets
    
    # estimate image width and image height throught ftbrd_box_w and ftbrd_box_h from
    # get_basic_params function (3rd out tuple parameter, basic_params[2])
    # note: for shorter notation ftbrd_box_w and ftbrd_box_h are fbox_w and fbox_h
    basic_params = draw_fretbrd.get_basic_params(radius_factor, lntk, ns, nf, fd, sd,
                     fret0, enable_header, enable_footer, enable_barre, enable_fretnum)
    radius = basic_params[0]
    fbox_w, fbox_h = basic_params[2]
    
    # empiric adjustments for label_offest
    label_offest = (radius * 0.9)
    
    # if chord is horizontal invert fbox_w, fbox_h
    if horiz: fbox_w, fbox_h = fbox_h, fbox_w
    
    # chord label width and height estimation
    # first tentative set label_h and presume to get label_w from label_h
    label_from_h = True
    
    # empiric adjustaments for label dimensions
    valid_multiline, _ = mymultilabels.isvalid_multiline(chord_name)
    if valid_multiline:
        label_h = fd * 2 * chord_label_font_factor
    else:
        label_h = fd * chord_label_font_factor
    
    
    # from label_h get label_w
    _, label_w = mymultilabels.get_multilabel_w_given_hght(chord_name, label_h, font_family) 

    # but if label_w does exceed fbox_w then set label_w to max (fbox_w)
    # and get label_h from label_w. Bool Flag label_from_h then is False
    if label_w > fbox_w:
        label_w = fbox_w
        _, label_h = mymultilabels.get_multilabel_h_given_wdth(chord_name, label_w, font_family)
        label_from_h = False
    
   
    # offset from bottom drawing and bottom image border
    bottom_offset = (1.0 * y_or)
    # offset from right side drawing and right side image border
    right_side_offset = (1.0 * x_or)
    
    # set image_w and image_h
    image_w = x_or + fbox_w + right_side_offset
    image_h = y_or + label_h + label_offest + fbox_h + bottom_offset

    # create dwg object
    dwg = svgwrite.Drawing(size=(image_w, image_h))
    
    # check if main chord label is left aligned and
    # set appropriate x center coordinate
    # for mylabel_given_xxxx() function
    if chord_label_isleft:
        label_x = (label_w / 2) + x_or
        center_flag = False
    else:
        label_x = (image_w / 2)
        center_flag = True
    
    # check if main chord label goes bottom or up
    # if main chord label goes at the bottom
    if chord_label_isbottom:
        # draw main chord label with correct x,y (center) bottom position
        # use appropriate function (based on bool var label_from_h) to draw label
        if label_from_h:
            mymultilabels.my2linelabel_given_hght(
                dwg,
                (label_x, 
                 y_or + label_offest + fbox_h + (label_h / 2)),
                chord_name, label_h,
                chord_label_font_weight, chord_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
        else:
            mymultilabels.my2linelabel_given_wdth(
                dwg,
                (label_x, 
                 y_or + label_offest + fbox_h + (label_h / 2)),
                chord_name, label_w,
                chord_label_font_weight, chord_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )  
    # if main chord label goes over the top
    else:
        # draw main chord label with correct x,y (center) upper position
        # use appropriate function (based on bool var label_from_h) to draw label
        if label_from_h:
            mymultilabels.my2linelabel_given_hght(
                dwg,
                (label_x, 
                 y_or + (label_h / 2)),
                chord_name, label_h,
                chord_label_font_weight, chord_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
        else:
            mymultilabels.my2linelabel_given_wdth(
                dwg,
                (label_x, 
                 y_or + (label_h) / 2),
                chord_name, label_w,
                chord_label_font_weight, chord_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
        # to draw chord under top main label, you need to 
        # offset down y_or to have space for main chord label
        y_or = y_or + label_h + label_offest

    # dlabels default to fingers if enable_dotlabels is true and dlabels is empty
    if enable_dotlabels and (dlabels == []):
        if fingers:
            dlabels = fingers
        # if fingers is empty then dlabels default to intervals
        elif (intervals != []):
            # remove 'h' char in intervals if present (used for formatting)
            intervals_flt = [intrv[:-1] if intrv[-1].lower()=='h' else intrv for intrv in intervals]
            dlabels = intervals_flt
   
    # get all chord params draw
    (
        radius,
        (x0, y0),
        (ftbrd_w, ftbrd_h),
        (ftbrd_box_w, ftbrd_box_h),
        horiz_lines_vertex,
        vertcl_lines_vertex,
        centers_matrix,
        upper_labels_centers_vector,
        side_labels_centers_vector,
        bottom_labels_centers_vector
    ) = draw_fretbrd.get_crd_params(x_or, y_or, radius_factor, lntk, ns, nf, fd, sd,
                       fret0, enable_header, enable_footer,
                       horiz, enable_barre, enable_fretnum)

    draw_chord_box(frets, fingers, intervals, dlabels, footer,
               radius, centers_matrix, upper_labels_centers_vector,
               bottom_labels_centers_vector, side_labels_centers_vector,
               horiz_lines_vertex, vertcl_lines_vertex, (ftbrd_box_w, ftbrd_box_h),
               dwg, nutline, fret0, enable_header, enable_dotlabels,
               enable_footer, enable_barre, enable_fretnum,
               barre_strk_wdth, horiz, 
               fretb_format, fret0_format,
               upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
               bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
               side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
               lntk, x_or, y_or, ns, nf, fd, edge_debug=debug,
               )
    
    return dwg, (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h), 


def chord_to_file(
        chord_name, chord_filename, frets, fingers, intervals, dlabels, footer,
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
        ):
    """
    create single complete chord svg file
    
    chord_name: String, chord name
    chord_filename: String, chord file name
    frets: List of strings, fret sequence
    fingers: List of strings, finger numbers list
    intervals: List of strings, interval sequence
    dlabels: List of strings, dot labels sequence
    footer: List of strings, footer sequence
    dir_output: String, output dir for chord image
    horiz: Boolean, if true chord is horizontal otherwise vertical
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels
    barre_strk_wdth: Number, barre arc tickness
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    font_weight: String, font weight
    font_family: String, font family
    chord_label_font_weight: String, Main chord label, font weight
    chord_label_font_family: String, Main chord label, font family
    chord_label_isbottom: Boolean, if true chord main label goes at the bottom
    chord_label_isleft: Boolean, if true chord main label is left aligned otherwise is centered
    xxx_format: Dict,
             interval: String, apply format to this interval dot -> tuple (
             dot_radius_scale: Number, dot radius scale factor
             dot_fill: String, color inside dot
             dot_fill_opacity: String, Dot fill opacity value
             dot_stroke: String, dot stroke width
             dot_stroke_opacity: String, Dot stroke fill opacity value
             dot_stroke_dasharray: String, dot stroke pattern of dashes and gaps,
                                   'dashes' to enable and None to disable
             dot_stroke_width: String, dot stroke width
             label_fill: String, label color
             label_fill_opacity: String, label fill opacity value
             dot_labelfont_weight: String, label font weight
             dot_labelfont_family: String, label font family
             dot_isquare: Boolean, if true draw square
             dot_rotate: Boolean, if true rotate dot by 90 deg
         )
         dicts are:
             fretb_format, for fretboard dots (fret >= 1)
             fret0_format, for fret0 dots (fret = 0)
    upper_labels_font_weight: String, upper labels, font weight
    upper_labels_font_family: String, upper labels, font family 
    upper_labels_font_factor: Number, upper labels, font size factor 
    bottom_labels_font_weight: String, bottom labels, font weight
    bottom_labels_font_family: String, bottom labels, font family   
    bottom_labels_font_factor: Number, bottom labels, font size factor      
    side_labels_font_weight: String, side labels, font weight
    side_labels_font_family: String, side labels, font family 
    side_labels_font_factor: Number, side labels, font size factor  
    x_or: Number, fretboard box origin (x)
    y_or: Number, fretboard box origin(y)  
    lntk: Number, grid line tickness    
    ns: Number, number of strings, is 6 for guitar
    nf: Number, number of frets, should be no more than 4 for chords
    fd: Number, fret distance (px)  
    sd: Number, string distance, optimal ratio is fd/sd = 1.2
    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41
    debug: Boolean, if true draw debug borders and debug dots

    return 3 tuples 
        (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h) just for debugging
    """    
    
    # call draw_chord() to draw chord
    dwg, (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h) = draw_chord(
        chord_name, frets, fingers, intervals, dlabels, footer,
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

    # if chord_filename is null then chord_filename = chord_name, otherwise use it 
    chord_filename = chord_name if (not chord_filename) else chord_filename
    
    # sanitize scale filename
    chord_filename = global_utilities.sanitize_str(chord_filename)
    
    # write svg file to disk
    chord_filename_path = dir_output + chord_filename + '.svg'
    dwg.saveas(filename=chord_filename_path)
  
    return (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h),


if __name__ == "__main__":
    
    # testing this functions
    
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
    
    # --- cli parameters ---
    dir_output = '../dirout/'        # output dir for chord image
    horiz = False                     # if true chord is horizontal otherwise vertical
    chord_label_isbottom = False     # if true chord main label goes at the bottom
    chord_label_isleft = False       # if true chord main label is left aligned otherwise is centered
    enable_header = True             # if True enable header labels
    enable_dotlabels = True          # if True enable dot labels
    enable_footer = True             # if True enable footer labels
    enable_barre = True              # if true draw barre/s on chord
    enable_fretnum = True            # if true enable side labels
    nutline = True                   # if True draw nut line ticker
    fret0 = True                     # if True you can draw dots above nut  
    font_weight = 'bold'             # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono'      # global font family: ['Courier New' | 'Ubuntu Mono' |  'DejaVu Sans Mono' | 'Liberation Mono']
    fret0_format = {}                # fret0_format, for fret0 dots
    fretb_format = {}                # fretb_format, for fretboard dots    
    chord_label_font_weight = None   # main chord label, font weight
    chord_label_font_family = None   # main chord label, font family
    chord_label_font_factor = None   # main chord label, font size factor: default is 0.70
    upper_labels_font_weight = None  # upper labels, font weight
    upper_labels_font_family = None  # upper labels, font family   
    upper_labels_font_factor = None  # upper labels, font size factor: default is 1.15
    bottom_labels_font_weight = None # bottom labels, font weight
    bottom_labels_font_family = None # bottom labels, font family      
    bottom_labels_font_factor = None # bottom labels, font size factor: default is 1.00
    side_labels_font_weight = None   # side labels, font weight
    side_labels_font_family = None   # side labels, font family
    side_labels_font_factor = None   # side labels, font size factor: default is 0.90


    args = (dir_output, horiz,
            enable_header, enable_dotlabels, enable_footer,
            enable_barre, enable_fretnum, barre_strk_wdth, nutline, fret0,
            font_weight, font_family,
            chord_label_font_weight, chord_label_font_family, 
            chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
            fretb_format, fret0_format,
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
            )
    
    # test chords
    chord_to_file(
          'XXX', ''
        , [' ', ' ', '0', 'x', 'x', 'x'], [], [], [], []
        , *args)
    chord_to_file(
          'YYY', ''
        , ['10', '10', '12', '12', '11', '10'], ['1', '1', '3', '4', '2', '1'] , ['R', '5', 'R', 'R', '3', '5'],
          ['R', '5', 'R', '1', '3', '5'], ['1', '1', '3', '4', '2', '1']
        , *args)
    chord_to_file(
          'SO', ''
        , ['x', '4', '6', '6', '6', '8'], ['x', '1', '3', '3', '3', '4'], ['x', 'R', '5', 'b7', 'b3', '5']
        , ['x', 'R', '5', 'm7', 'm3', '5'], ['x', '1', '3', '3', '3', '4']
        , *args)
    chord_to_file(
          'SOLdij7b5', ''
        , ['X', '3', '2', '0', '1', '1'], ['X', '3', '2', 'X', '1', '1'], ['X', 'R', '3', '5', 'R', '4']
        , ['X', 'R', '3', '5', '1', '4'], ['x', '3', '2', 'X', '1', '1']
        , *args)
    chord_to_file(
          'SQj+', ''
        , ['3', '3', 'x', '0', '1', '0'], ['3', '3', 'x', 'x', '1', 'x'], []
        , [], ['C', 'I', 'A', 'O', 'N', 'E']
        , *args)
    chord_to_file(
          'SO#maj7', ''
        , ['x', '4', '6', '5', '6', '4'], ['x', '1', '2', '3', '4', '1'], ['X', 'R', '5', '7', '3', '5']
        , ['X', 'R', '5', '7', '3', '5'], ['x', '1', '2', '3', '4', '1']
        , *args)
    chord_to_file(
          'SOmaj7 nice\nBeautiful land', ''
        , ['x', '3', '2', '0', '0', '0'], ['x', '3', '2', 'x', 'x', 'x'], ['x', 'R', '5', '7', '3', '5']
        , ['x', 'R', '5', '7', '3', '5'], ['x', '3', '2', 'x', 'x', 'x']
        , *args)    
    chord_to_file(
          'SI11', ''
        , ['x', '0', '9', '8', '0', '0'],  ['x', 'x', '2', '1', 'x', 'x'], ['x', '7', 'R', '3', 'R', '11']
        , ['x', '7', 'R', '3', 'R', '11'], ['x', 'x', '2', '1', 'x', 'x']
        , *args)  
