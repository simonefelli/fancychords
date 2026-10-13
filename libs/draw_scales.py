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
draw_scales: draw a complete scale diagram and save it as an svg file.

It reuses the chord drawing blocks (draw_fretbrd, draw_dots, mylabels) with
two differences from chords: a scale can span many frets (the fretboard is
as long as the scale) and its notes are given per string, as a matrix
strgs_frets_list[string][column]. Call chain:

    scale_to_file()     draw the scale with draw_scale() and save it to disk
    draw_scale()        fill in default formats and fonts, compute the image
                        size, create the svgwrite Drawing, draw the main label
    draw_scale_box()    fretboard, dots (draw_dots.draw_scale_dots), arrows,
                        upper/bottom labels and side fret numbers
                        (scales_side_labels)
"""

# third party imports
import svgwrite

# local application imports
from libs import mylabels
from libs import mymultilabels
from libs import global_utilities
from libs import draw_dots
from libs import draw_fretbrd


def scales_side_labels(first_fret, max_fret, legacy=False):
    '''
    Compute side labels string list for scales.
    Plan is: if scale start from nut follow guitar neck dots logic.
    If scale start from a certain fret begin with that fret and continue
    with guitar neck dots logic, but leave an empty fret from the first.
    If legacy is Ture follow chords logic: if scale start from nut only
    3rd fret is labelled. If scale start from a certain fret begin 
    with that fret only
    
    first_fret: Number, first fret of scale
    max_fret: Number, max fret of scale
    legacy: Boolean, if true the function behaves as for chords
    
    return: List, side label string list
    '''
    if legacy:
        complete_side_labels =  [
            None, None, 
            '3',  None, 
            None, None, 
            None, None, 
            None, None, None, 
            None, None, None, 
            None, None, 
            None, None, 
            None, None, 
            None
        ]
    else:
        complete_side_labels =  [
            None, None, 
            '3',  None, 
            '5',  None, 
            '7',  None, 
            '9',  None, None, 
            '12', None, None, 
            '15', None, 
            '17', None, 
            '19', None, 
            '21', None,
            None, '24'
        ]
    # complete_side_labels[i] is the label of fret i+1, it covers every fret
    # allowed in a scale file (1..24). Before, the list stopped at fret 21 and
    # scales above it crashed with IndexError
    if legacy: complete_side_labels += [None, None, None]
    final_side_labels = complete_side_labels[:max_fret]
    if first_fret > 0:
        # first fret always shows its own number...
        final_side_labels[first_fret-1] = str(first_fret)
        # ...and the next fret is left empty, so two numbers are never side by side.
        # The check is needed when the scale uses just one fret
        # (first_fret == max_fret): there is no next fret and it used to crash
        if first_fret < len(final_side_labels):
            final_side_labels[first_fret] = None
        # drop the frets before first_fret (they are not drawn)
        final_side_labels = final_side_labels[first_fret-1:]  
    return final_side_labels


def draw_scale_box(
        strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, footer, arrows,
        radius, centers_matrix,
        upper_labels_centers_vector, bottom_labels_centers_vector,
        side_labels_centers_vector, horiz_lines_vertex, vertcl_lines_vertex,
        ftbrd_box_wh, dwg, nutline, fret0, enable_header, enable_dotlabels,
        enable_footer, enable_fretnum, horiz,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor
        , lntk
        , x_or
        , y_or
        , ns
        , edge_debug
        ):
    """
    Draw single scale image with dots, labels, headers, footer
    and side labels (NO scale name main label)

    strgs_frets_list: list of string lists (6 elements, one for every guitar String - frets positions)
        ie: [['5', '5', '5', '5', '5', '5'], ['x', '6', 'x', 'x', 'x', 'x'], ...]
    strgs_intervals_list: list of string lists (6 elements, one for every guitar String - intervals positions), optional
        ie: [['R', '4', 'b7', 'b3', '5', 'R'], ['x', 'b5', 'x', 'x', 'x', 'x'], ...]
    strgs_dlabels_list: list of string lists (6 elements, one for every guitar String - dlabels positions), optional
        ie: [['1', '1', '1', '1', '1', '1'], ['x', '2', 'x', 'x', 'x', 'x'], ...]
    footer: List of strings, footer sequence
    arrows: List of 2-tuple of 2-tuple representing an arrows sequence
                [(arrow1), (arrow2), (arrow3), ...] =
                [(start_point1, end_point1), (start_point2, end_point2), ...] =
                [((start_Fret1, start_String1), (end_Fret1, end_String1)), ((start_Fret2, start_String2), ...]
    radius: Number, dot radius in scale image
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
    enable_fretnum: Boolean, if true enable side labels
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
    arrows_format: Tuple,
        (arrows stroke width, arrows stroke color, arrows stroke opacity, start_end_flag, bezier, arrow_stroke_dasharray)
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
    nf: Number, number of frets
    edge_debug: Boolean, if true draw debug borders and debug dots

    return nothing
    """
    (ftbrd_box_w, ftbrd_box_h) = ftbrd_box_wh

    # calculate max fret number and min fret number for the whole frets_list matrix
    # using global_utilities.max_min_scales_slst()
    max_fret, min_fret = global_utilities.max_min_scales_slst(strgs_frets_list)

    nut = False
    first_fret = min_fret
    if (first_fret == 0) and nutline:   # if first_fret = 0 draw nut is allowed
        nut = True                      # but before check if nutline variable is True and after that 
                                        # you can set nut to true to draw nut on fretboard
                                        
    # compute side_labels with scales_side_labels function
    side_labels = scales_side_labels(first_fret, max_fret)
    
    # transpose scale strgs_frets_list to have a list of 1 fret chords
    transp_frets_list = global_utilities.traspose_fretb(strgs_frets_list)

    # if header is present
    if enable_header:
        # only first element of transp_frets_list count because open Strings
        # are at left so only the first 1 fret chord can have 0s
        frets = transp_frets_list[0]
        # if draw dots above nut flag is true then no upper labels (no 'x' for scales above nut)
        # upper header: ['x','3','2','0','1','0'] -> [None,None,None,None,None,None] 
        if fret0:
            # header = [fr if (not fr.isdigit()) else None for fr in frets]
            header = None
        else:
        # if you do not draw dots above nut upper labels should be only '0'
        # upper header: ['x','3','2','0','1','0'] -> [None,None,None,'0',None,'0']            
            header = [fr if (fr.isdigit() and int(fr) == 0) else None for fr in frets]
    else:
        # else do not draw header
        header = None
    # if enable_dotlabels is false do not draw dot labels
    if not enable_dotlabels: strgs_dlabels_list = []
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
    draw_dots.draw_scale_dots(strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, 
                    radius, fret0, first_fret, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                    )

    # draw arrows
    if arrows:
        (line_stroke_wdth, line_stroke_color, line_stroke_opacity, 
         start_end_flag, bezier, arrow_stroke_dasharray) = arrows_format
        for arrow in arrows:
            draw_dots.myarrow(
                arrow[0], arrow[1], radius, 
                fret0, first_fret, centers_matrix, horiz, 
                line_stroke_wdth, line_stroke_color, line_stroke_opacity, 
                start_end_flag, bezier, arrow_stroke_dasharray, dwg, ns)

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
        # make all sidelabel same size setting label_len_is_h to True.
        # If not, 2digit numbers will be smaller (to fit same width)
        # This logic is different from the one of draw_chord_box() function
        label_len_is_h = True
        mylabels.draw_labels(side_labels, (radius * side_labels_font_factor), 
                             side_labels_centers_vector, dwg,
                             side_labels_font_weight, side_labels_font_family,
                             label_len_is_h=label_len_is_h)


def draw_scale(
        scale_name, strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, footer, arrows,
        horiz, enable_header, enable_dotlabels, enable_footer, enable_fretnum,
        nutline, fret0, font_weight, font_family,
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,  
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        ):
    """
    draw a single scale, complete with scale name main label. Set also default formatting
    
    scale_name: String, scale name
    strgs_frets_list: list of string lists (6 elements, one for every guitar String - frets positions)
        ie: [['5', '5', '5', '5', '5', '5'], ['x', '6', 'x', 'x', 'x', 'x'], ...]
    strgs_intervals_list: list of string lists (6 elements, one for every guitar String - intervals positions), optional
        ie: [['R', '4', 'b7', 'b3', '5', 'R'], ['x', 'b5', 'x', 'x', 'x', 'x'], ...]
    strgs_dlabels_list: list of string lists (6 elements, one for every guitar String - dlabels positions), optional
        ie: [['1', '1', '1', '1', '1', '1'], ['x', '2', 'x', 'x', 'x', 'x'], ...]
    footer: List of strings, footer sequence
    arrows: List of 2-tuple of 2-tuple representing an arrows sequence
                [(arrow1), (arrow2), (arrow3), ...] =
                [(start_point1, end_point1), (start_point2, end_point2), ...] =
                [((start_Fret1, start_String1), (end_Fret1, end_String1)), ((start_Fret2, start_String2), ...]
    horiz: Boolean, if true scale is horizontal otherwise vertical
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_fretnum: Boolean, if true enable side labels
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    font_weight: String, font weight
    font_family: String, font family
    scale_label_font_weight: String, Main scale label, font weight
    scale_label_font_family: String, Main scale label, font family
    scale_label_font_factor: Number, Main scale label, font size factor
    scale_label_isbottom: Boolean, if true scale main label goes at the bottom
    scale_label_isleft: Boolean, if true scale main label is left aligned
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
    arrows_format: Tuple,
        (arrows stroke width, arrows stroke color, arrows stroke opacity, start_end_flag, bezier, arrow_stroke_dasharray)
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
    nf: Number, number of frets, should be no more than 4 for scales
    fd: Number, fret distance (px)  
    sd: Number, string distance, optimal ratio is fd/sd = 1.2
    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41
    debug: Boolean, if true draw debug borders and debug dots

    return dwg object (needed) and 
        3 tuples (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h) just for debugging
    """

    # fretb_format and fret0_format default formats if note set. Moreover
    # if specific element (dot_label, scale_label, upper_labels) font_weight or font_family
    # are not set then default to global font_weight and font_family
    
    # xxx_format tuples formats (13 elements, see fancychords.py for details):
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
    
    # fretb_format: every format default to global font_weight and font_family
    # if not set (see global_utilities.fill_format_fonts())
    fretb_format = global_utilities.fill_format_fonts(fretb_format, font_weight, font_family)

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
    
    # fret0_format: every format default to global font_weight and font_family
    # if not set. Note: fonts are elements 9 and 10 of the 13 elements tuple
    # (this code used 6 and 7, left over from an older 10 elements tuple, so
    # fret0 dot labels never got the global font)
    fret0_format = global_utilities.fill_format_fonts(fret0_format, font_weight, font_family)


    # arrows_format default
    # -------------------------
    # (
    #   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
    #  )
    if not arrows_format:
        arrows_format = (lntk, 'black', '1.0', 'e', True, '')
    
    # other font variables
    if not scale_label_font_weight: scale_label_font_weight = font_weight
    if not scale_label_font_family: scale_label_font_family = font_family
    if not scale_label_font_factor: scale_label_font_factor = 0.80
    if not upper_labels_font_weight: upper_labels_font_weight = font_weight
    if not upper_labels_font_family: upper_labels_font_family = font_family
    if not upper_labels_font_factor: upper_labels_font_factor = 1.15
    if not bottom_labels_font_weight: bottom_labels_font_weight = font_weight
    if not bottom_labels_font_family: bottom_labels_font_family = font_family
    if not bottom_labels_font_factor: bottom_labels_font_factor = 0.80
    if not side_labels_font_weight: side_labels_font_weight = font_weight
    if not side_labels_font_family: side_labels_font_family = font_family
    if not side_labels_font_factor: side_labels_font_factor = 0.70

    # check if fretboard number of frets are enough considering input frets list
    
    # calculate max fret number and min fret number for the whole strgs_frets_list matrix
    # using max_min_scales_slst() which take into account also zeros and 'x':
    # min_fret can be 0, as opposed to chords as they use max_min_fret_slst() function
    # this is because we want to be possible to draw the neck from the nut
    max_fret, min_fret = global_utilities.max_min_scales_slst(strgs_frets_list)
    
    # now if min_fret can be 0 we must compensate delta_frets
    if min_fret == 0:
        # compensate with a + 1
        delta_frets = max_fret - min_fret
    else:
        # regular case as chords
        delta_frets = max_fret - min_fret + 1
        
    # if not enough then set nf = delta_frets
    if (delta_frets) > nf: nf = delta_frets
    
    # estimate image width and image height throught ftbrd_box_w and ftbrd_box_h from
    # get_basic_params function (3rd out tuple parameter, basic_params[2])
    # note: for shorter notation ftbrd_box_w and ftbrd_box_h are fbox_w and fbox_h
    basic_params = draw_fretbrd.get_basic_params(radius_factor, lntk, ns, nf, fd, sd,
                     fret0, enable_header, enable_footer, False, enable_fretnum)
    radius = basic_params[0]
    fbox_w, fbox_h = basic_params[2]
    
    # empiric adjustments for label_offest
    label_offest = (radius * 0.9)
    
    # if scale is horizontal invert fbox_w, fbox_h
    if horiz: fbox_w, fbox_h = fbox_h, fbox_w
    
    # scale label width and height estimation
    # first tentative set label_h and presume to get label_w from label_h
    label_from_h = True
    
    # empiric adjustaments for label dimensions
    valid_multiline, _ = mymultilabels.isvalid_multiline(scale_name)
    if valid_multiline:
        if horiz:
            label_h = fd * scale_label_font_factor
        else:
            label_h = fd * scale_label_font_factor
    else:
        if horiz:
            label_h = fd * scale_label_font_factor * 0.40
        else:
            label_h = fd * scale_label_font_factor * 0.40
    
    # from label_h get label_w
    # note: label is measured with the same font used to draw it
    _, label_w = mymultilabels.get_multilabel_w_given_hght(scale_name, label_h, scale_label_font_family)
    
    # but if label_w does exceed fbox_w then set label_w to max (fbox_w)
    # and get label_h from label_w. Bool Flag label_from_h then is False
    if label_w > fbox_w:
        label_w = fbox_w
        _, label_h = mymultilabels.get_multilabel_h_given_wdth(scale_name, label_w, scale_label_font_family)
        label_from_h = False

    # offset from bottom drawing and bottom image border
    bottom_offset = (1.0 * y_or)
    # offset from right side drawing and right side image border
    right_side_offset = (1.0 * x_or)
    
    # set image_w and image_h
    image_w = x_or + fbox_w + right_side_offset
    image_h =  y_or + label_h + label_offest + fbox_h + bottom_offset

    # create dwg object
    dwg = svgwrite.Drawing(size=(image_w, image_h)) 

    # check if main scale label is left aligned and
    # set appropriate x center coordinate and center_flag
    # for my2linelabel_given_xxxx() function
    if scale_label_isleft:
        label_x = (label_w / 2) + x_or
        center_flag = False
    else:
        label_x = (image_w / 2)
        center_flag = True

    # check if main scale label goes bottom or up
    # if main scale label goes at the bottom
    if scale_label_isbottom:
        # draw main scale label with correct x,y (center) bottom position
        # use appropriate function (based on bool var label_from_h) to draw label
        if label_from_h:
            mymultilabels.my2linelabel_given_hght(
                dwg,
                (label_x, 
                 y_or + label_offest + fbox_h + (label_h / 2)),
                scale_name, label_h,
                scale_label_font_weight, scale_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
        else:
            mymultilabels.my2linelabel_given_wdth(
                dwg,
                (label_x, 
                 y_or + label_offest + fbox_h + (label_h / 2)),
                scale_name, label_w,
                scale_label_font_weight, scale_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
    # if main scale label goes over the top
    else:
        # draw main scale label with correct x,y (center) upper position
        # use appropriate function (based on bool var label_from_h) to draw label
        if label_from_h:
            mymultilabels.my2linelabel_given_hght(
                dwg,
                (label_x, 
                 y_or + (label_h / 2)),
                scale_name, label_h,
                scale_label_font_weight, scale_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
        else:
            mymultilabels.my2linelabel_given_wdth(
                dwg,
                (label_x, 
                 y_or + (label_h) / 2),
                scale_name, label_w,
                scale_label_font_weight, scale_label_font_family,
                align_center_flag = center_flag, 
                edge_debug=debug
                )
        # to draw scale under top main label, you need to 
        # offset down y_or to have space for main scale label
        y_or = y_or + label_h + label_offest

    # dlabels default to intervals if enable_dotlabels is true and dlabels is empty
    if enable_dotlabels and (strgs_dlabels_list == []):
        if strgs_intervals_list:
            # remove 'h' char in intervals if present (used for formatting)
            intervals_flt = []
            for intervals in strgs_intervals_list:
                intervals_flt.append([intrv[:-1] if intrv[-1].lower()=='h' else intrv for intrv in intervals])
            strgs_dlabels_list = intervals_flt
   
    # get all scale params draw
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
                       horiz, False, enable_fretnum)

    draw_scale_box(
        strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, footer, arrows,
        radius, centers_matrix,
        upper_labels_centers_vector, bottom_labels_centers_vector,
        side_labels_centers_vector, horiz_lines_vertex, vertcl_lines_vertex,
        (ftbrd_box_w, ftbrd_box_h), dwg, nutline, fret0, enable_header, enable_dotlabels,
        enable_footer, enable_fretnum, horiz,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor
        , lntk
        , x_or
        , y_or
        , ns
        , debug
        )
     
    return dwg, (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h), 


def scale_to_file(
        scale_name, scale_filename, strgs_frets_list, 
        strgs_intervals_list, strgs_dlabels_list, footer, arrows, 
        dir_output, horiz, enable_header, enable_dotlabels, 
        enable_footer, enable_fretnum, nutline, 
        fret0, font_weight, font_family, 
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        ):
    """
    create single complete scale svg file
    
    scale_name: String, scale name
    scale_filename: String, scale file name
    strgs_frets_list: list of string lists (6 elements, one for every guitar String - frets positions)
        ie: [['5', '5', '5', '5', '5', '5'], ['x', '6', 'x', 'x', 'x', 'x'], ...]
    strgs_intervals_list: list of string lists (6 elements, one for every guitar String - intervals positions), optional
        ie: [['R', '4', 'b7', 'b3', '5', 'R'], ['x', 'b5', 'x', 'x', 'x', 'x'], ...]
    strgs_dlabels_list: list of string lists (6 elements, one for every guitar String - dlabels positions), optional
        ie: [['1', '1', '1', '1', '1', '1'], ['x', '2', 'x', 'x', 'x', 'x'], ...]
    footer: List of strings, footer sequence
    arrows: List of 2-tuple of 2-tuple representing an arrows sequence
                [(arrow1), (arrow2), (arrow3), ...] =
                [(start_point1, end_point1), (start_point2, end_point2), ...] =
                [((start_Fret1, start_String1), (end_Fret1, end_String1)), ((start_Fret2, start_String2), ...]
    dir_output: String, output dir for scale image
    horiz: Boolean, if true scale is horizontal otherwise vertical
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_fretnum: Boolean, if true enable side labels
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    font_weight: String, font weight
    font_family: String, font family
    scale_label_font_weight: String, Main scale label, font weight
    scale_label_font_family: String, Main scale label, font family
    scale_label_font_factor: Number, Main scale label, font size factor
    scale_label_isbottom: Boolean, if true scale main label goes at the bottom
    scale_label_isleft: Boolean, if true scale main label is left aligned
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
    arrows_format: Tuple,
        (arrows stroke width, arrows stroke color, arrows stroke opacity, start_end_flag, bezier, arrow_stroke_dasharray)
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
    nf: Number, number of frets
    fd: Number, fret distance (px)  
    sd: Number, string distance, optimal ratio is fd/sd = 1.2
    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41
    debug: Boolean, if true draw debug borders and debug dots

    return dwg object (needed) and 
        3 tuples (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h) just for debugging
    """    
    
    # call draw_scale() to draw scale
    dwg, (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h) = draw_scale(
        scale_name, strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, footer, arrows,
        horiz, enable_header, enable_dotlabels, enable_footer, enable_fretnum,
        nutline, fret0, font_weight, font_family,
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
    )

    # if scale_filename is null then scale_filename = scale_name, otherwise use it 
    scale_filename = scale_name if (not scale_filename) else scale_filename
    
    # sanitize scale filename
    scale_filename = global_utilities.sanitize_str(scale_filename)
    
    # write svg file to disk
    scale_filename_path = dir_output + scale_filename + '.svg'
    dwg.saveas(filename=scale_filename_path)
  
    return (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h),



if __name__ == "__main__":
    
    # testing this functions

    # --- internal parameters ---
    
    sd = 55.00                      # string distance, optimal ratio is fd/sd = 1.30 - 1.40
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings
    nf = 4                          # number of frets    
    debug = True                    # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.40                  # fret distance                                
    radius_factor = 22.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples
                                    
    dir_output = '../dirout/'        # output dir for scale image
    scale_label_isbottom = False     # if true scale main label goes at the bottom
    scale_label_isleft = True       # if true scale main label is left aligned otherwise is centered
    enable_header = True             # if True enable header labels
    enable_dotlabels = True          # if True enable dot labels     
    enable_footer = True             # if True enable footer labels
    enable_fretnum = True            # if true enable side labels
    nutline = True                   # if True draw nut line ticker   
    font_weight = 'normal'           # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono'      # global font family: ['Courier New' | 'Ubuntu Mono' |  'DejaVu Sans Mono' | 'Liberation Mono']
    fret0_format = {}                # fret0_format, for fret0 dots
    fretb_format = {}                # fretb_format, for fretboard dots
    scale_label_font_weight = None   # main scale label, font weight
    scale_label_font_family = None   # main scale label, font family
    scale_label_font_factor = None   # main scale label, font size factor: default is 0.50
    upper_labels_font_weight = None  # upper labels, font weight
    upper_labels_font_family = None  # upper labels, font family   
    upper_labels_font_factor = None  # upper labels, font size factor: default is 1.15
    bottom_labels_font_weight = None # bottom labels, font weight
    bottom_labels_font_family = None # bottom labels, font family      
    bottom_labels_font_factor = None # bottom labels, font size factor: default is 0.80
    side_labels_font_weight = None   # side labels, font weight
    side_labels_font_family = None   # side labels, font family
    side_labels_font_factor = None   # side labels, font size factor  : default is 0.70
    
    # arrows_format default
    # -------------------------
    # (
    #   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
    #  )
    arrows_format = (lntk, 'black', '1.0', 'e', True, '')    
    

    # ---  test for scale_to_file  ---
    
    fret0 = False
    horiz = False
    args = (
        dir_output, horiz, enable_header, enable_dotlabels, 
        enable_footer, enable_fretnum, nutline, 
        fret0, font_weight, font_family, 
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        )
    scale_to_file(
          'Am Blues Pentatonic Scale\nPosition 1, Blue Note Missing', 'test_movable_penta'
        , [
              ['5', 'x', 'x', '8']
            , ['5', 'x', 'x', '8']
            , ['5', 'x', '7', '8']
            , ['5', 'x', '7', 'x']
            , ['5', '6', '7', 'x']
            , ['5', 'x', 'x', '8']
        ]
        , [
              ['R', 'x', 'x', 'b3']
            , ['5', 'x', 'x', 'b7']
            , ['b3', 'x', '4', 'b5']
            , ['b7', 'x', 'R', 'x']
            , ['4', 'b5', '5', 'x']
            , ['R', 'x', 'x', 'b3']
        ]
        , [
              ['1', 'x', 'x', '4']
            , ['1', 'x', 'x', '4']
            , ['1', 'x', '3', '4']
            , ['1', 'x', '3', 'x']
            , ['1', '2', '3', 'x']
            , ['1', 'x', 'x', '4']
        ]
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , [
              ((5,2), (8,2))
            , ((5,4), (7,4))
            , ((6,5), (7,5))
        ]
        , *args
        )


    fret0 = True
    horiz = True
    args = (
        dir_output, horiz, enable_header, enable_dotlabels, 
        enable_footer, enable_fretnum, nutline, 
        fret0, font_weight, font_family, 
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        )
    scale_to_file(
          'Am Blues Pentatonic Scale\nPosition 2, Blue Note Missing', 'test_open_penta'
        , [
              ['0', '1', 'x', '3']
            , ['0', '1', 'x', '3']
            , ['0', 'x', '2', 'x']
            , ['0', 'x', '2', '3']
            , ['0', 'x', '2', '3']
            , ['0', '1', 'x', '3']
        ]
        , [
              ['3', '4', 'x', '5']
            , ['7', 'R', 'x', '2']
            , ['5', 'x', '6', 'x']
            , ['2', 'x', '3', '4']
            , ['6', 'x', '7', 'R']
            , ['3', '4', 'x', '5']
        ]
        , [
              ['3', '4', 'x', '5']
            , ['7', 'R', 'x', '2']
            , ['5', 'x', '6', 'x']
            , ['2', 'x', '3', '4']
            , ['6', 'x', '7', 'R']
            , ['3', '4', 'x', '5']
        ]
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , [
              ((1,6), (3,6))
            , ((2,5), (3,5))
            , ((0,2), (3,2))
        ]
        , *args
        )


    fret0 = False
    horiz = False
    args = (
        dir_output, horiz, enable_header, enable_dotlabels, 
        enable_footer, enable_fretnum, nutline, 
        fret0, font_weight, font_family, 
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        )
    scale_to_file(
          'Am Blues', 'test_3'
        , [
              ['x', '8', 'x', '10', '11']
            , ['x', '8', 'x', '10', 'x']
            , ['7', '8', '9', 'x', 'x']
            , ['7', 'x', 'x', '10', 'x']
            , ['7', 'x', 'x', '10', 'x']
            , ['x', '8', 'x', '10', '11']
        ]
        , [
              ['x', 'b3', 'x', '4', 'b5']
            , ['x', 'b7', 'x', 'R', 'x']
            , ['4', 'b5', '5', 'x', 'x']
            , ['R', 'x', 'x', 'b3', 'x']
            , ['5', 'x', 'x', 'b7', 'x']
            , ['x', 'b3', 'x', '4', 'b5']
        ]
        , [
              ['x', '1', 'x', '3', '4']
            , ['x', '1', 'x', '3', 'x']
            , ['1', '2', '3', 'x', 'x']
            , ['1', 'x', 'x', '4', 'x']
            , ['1', 'x', 'x', '4', 'x']
            , ['x', '1', 'x', '3', '4']
        ]
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , []
        , *args
        )

    fret0 = True
    horiz = True
    args = (
        dir_output, horiz, enable_header, enable_dotlabels, 
        enable_footer, enable_fretnum, nutline, 
        fret0, font_weight, font_family, 
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        )
    scale_to_file(
          'Full Blues', 'full_blues'
        , [
              ['x','x','2','3','x','x','x','7','x','x','10','x' ,'x' ,'x','14','15','x' ]
            , ['0','x','x','3','x','x','x','7','8','x','x' ,'x' ,'12','x','x' ,'15','x' ]
            , ['0','x','x','x','4','x','x','7','x','x','x' ,'11','12','x','x' ,'x' ,'16']
            , ['0','x','x','x','4','5','x','x','x','9','x' ,'x' ,'12','x','x' ,'x' ,'16']
            , ['x','x','2','x','x','5','x','x','x','9','10','x' ,'x' ,'x','14','x' ,'x' ]
            , ['x','x','2','3','x','x','x','7','x','x','10','x' ,'x' ,'x','14','15','x' ]
        ]
        , []
        , []
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , []
        , *args
        )

    fret0 = True
    horiz = True
    args = (
        dir_output, horiz, enable_header, enable_dotlabels, 
        enable_footer, enable_fretnum, nutline, 
        fret0, font_weight, font_family, 
        scale_label_font_weight, scale_label_font_family, 
        scale_label_font_factor, scale_label_isbottom, scale_label_isleft,
        fretb_format, fret0_format, arrows_format,
        upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
        bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
        side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
        lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
        )
    scale_to_file(
          'Full Blues Partial', 'full_blues_partial'
        , [
              ['x','x','x','x','x','x','x','7','x','x','10','x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','7','8','x','x' ,'x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','7','x','x','x' ,'x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','x','x','9','x' ,'x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','x','x','9','10','x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','7','x','x','10','x','x','x','x','x','x']
        ]
        , []
        , []
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , []
        , *args
        )