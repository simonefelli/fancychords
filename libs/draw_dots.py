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


# local application imports
from libs import myshapes
from libs import mylabels
from libs import mydots
from libs import global_utilities


def myarrow(pt1, pt2, radius, 
            fret0, first_fret, centers_matrix, horiz,
            strk_wdth, line_stroke_color, line_stroke_opacity,
            start_end_flag, bezier, arrow_stroke_dasharray, dwg, ns):
    '''
    Draw a complete single/double arrow
    
    pt1: Tuple, start point (fret_number, string_number)
    pt2: Tuple, end point   (fret_number, string_number)
    radius: Number, dot radius in chord image
    fret0: Boolean, if true you can draw dots above nut    
    first_fret: Number, min fret number
    centers_matrix: List of List, dots centers matrix
    horiz: Boolean, if true adjust arrow to fit in a horizontal centers_matrix
    strk_wdth: Number, line stroke width
    line_stroke_color: String, line stroke color
    line_stroke_opacity: String, line fill opacity value
    start_end_flag: String, parameter to enable/disable arrowheads, ie:
        start_end_flag = ''   -> no arrowheads
        start_end_flag = 's'  -> start arrowheads
        start_end_flag = 'e'  -> end arrowheads
        start_end_flag = 'se' -> start and end arrowheads
    bezier: Boolean, if true draw a bezier curve (a small arc) instead of a straight line
    arrow_stroke_dasharray: String, dot stroke pattern of dashes and gaps
                            'dashes' to enable and None to disable
    dwg: Svgwrite object
    '''

    # if first_fret > 0 and new normalized fret is not negative or 0 then normalize 
    # fret number (we do not want negative numbers)
    if (first_fret > 0):
        # calculate shifted pt1 fret for candidate new normalized fret
        shifted_pt1 = pt1[0] - (first_fret) + 1
        # if shifted pt1 fret is > 0 then it can be the new normalized pt1 fret, else no normalization
        pt1 = (shifted_pt1, pt1[1]) if (shifted_pt1 > 0) else (pt1[0] , pt1[1])
        # calculate shifted pt2 fret for candidate new normalized fret
        shifted_pt2 = pt2[0] - (first_fret) + 1
        # if shifted pt2 fret is > 0 then it can be the new normalized pt2 fret, else no normalization
        pt2 = (shifted_pt2, pt2[1]) if (shifted_pt2 > 0) else (pt2[0] , pt2[1])

    
    # if fret0 is enabled adjust (dot_x, dot_y) 
    if fret0: 
        pt1_x = centers_matrix[pt1[0]][abs(pt1[1]-ns)][0]
        pt1_y = centers_matrix[pt1[0]][abs(pt1[1]-ns)][1]
        pt2_x = centers_matrix[pt2[0]][abs(pt2[1]-ns)][0]
        pt2_y = centers_matrix[pt2[0]][abs(pt2[1]-ns)][1]   
    else:
        pt1_x = centers_matrix[pt1[0]-1][abs(pt1[1]-ns)][0]
        pt1_y = centers_matrix[pt1[0]-1][abs(pt1[1]-ns)][1]  
        pt2_x = centers_matrix[pt2[0]-1][abs(pt2[1]-ns)][0]
        pt2_y = centers_matrix[pt2[0]-1][abs(pt2[1]-ns)][1] 


    # if centers_matrix is not horizontal
    if not horiz:
        
        sd = centers_matrix[0][1][0] - centers_matrix[0][0][0]
        fd = centers_matrix[1][0][1] - centers_matrix[0][0][1]
        #print(sd, fd)

        # offset arrow start/end points so they do not intersect dots,
        # calculate Bézier offset for quadratic curve
        
        # if pt1 and pt2 are horizontal on x
        if (pt2[0] - pt1[0]) == 0:
            pt1_offset_y = -1.0 * radius
            pt2_offset_y = -1.0 * radius
            pt_bzr_offset_y  = -0.6 * fd
        # if pt2 is below pt1
        elif (pt2[0] - pt1[0]) > 0:
            pt1_offset_y =  1.0 * radius
            pt2_offset_y = -1.0 * radius
            pt_bzr_offset_y  = 0
        # if pt2 is above pt1
        else:
            pt1_offset_y = -1.0 * radius
            pt2_offset_y =  1.0 * radius
            pt_bzr_offset_y  = 0
        
        # pt1 and pt2 are vertical on y
        if (pt2[1] - pt1[1]) == 0:
            pt1_offset_x = 1.0 * radius
            pt2_offset_x = 1.0 * radius
            pt_bzr_offset_x  = 0.6 * sd
        # if pt2 is at left of pt1    
        elif (pt2[1] - pt1[1]) < 0:
            pt1_offset_x =  1.0 * radius
            pt2_offset_x = -1.0 * radius
            pt_bzr_offset_x  = 0 
        # if pt2 is at right of pt1
        else:
            pt1_offset_x = -1.0 * radius
            pt2_offset_x =  1.0 * radius
            pt_bzr_offset_x  = 0

    # if centers_matrix is horizontal, swap x and y and adjust
    else:
        
        sd = centers_matrix[0][0][1] - centers_matrix[0][1][1]
        fd = centers_matrix[1][0][0] - centers_matrix[0][0][0]
        #print(sd, fd)

        # if pt1 and pt2 are vertical on x
        if (pt2[0] - pt1[0]) == 0:
            pt1_offset_x = -1.0 * radius
            pt2_offset_x = -1.0 * radius
            pt_bzr_offset_x = -0.6 * fd
        # if pt2 is right pt1
        elif (pt2[0] - pt1[0]) > 0:
            pt1_offset_x =  1.0 * radius
            pt2_offset_x = -1.0 * radius
            pt_bzr_offset_x = 0
        # if pt2 is left pt1
        else:
            pt1_offset_x = -1.0 * radius
            pt2_offset_x =  1.0 * radius
            pt_bzr_offset_x = 0
        
        # pt1 and pt2 are horizontal on y
        if (pt2[1] - pt1[1]) == 0:
            pt1_offset_y = -1.0 * radius
            pt2_offset_y = -1.0 * radius
            pt_bzr_offset_y = -0.6 * sd
        # if pt2 is above pt1    
        elif (pt2[1] - pt1[1]) < 0:
            pt1_offset_y = -1.0 * radius
            pt2_offset_y =  1.0 * radius
            pt_bzr_offset_y = 0 
        # if pt2 is below pt1
        else:
            pt1_offset_y =  1.0 * radius
            pt2_offset_y = -1.0 * radius
            pt_bzr_offset_y = 0 

    # if bezier is True draw an arc else a stright line (however diagonals
    # are straight lines)
    if bezier:
        # calculate Q value of bezier curve as 
        # bez_median = median point + offset
        bez_median = (
              ((pt1_x + pt2_x) / 2) + pt_bzr_offset_x
            , ((pt1_y + pt2_y) / 2) + pt_bzr_offset_y
            )
    else:
        bez_median = None   

    # draw arrow
    myshapes.basic_arrow(
          dwg
        , (pt1_x + pt1_offset_x, pt1_y + pt1_offset_y)
        , (pt2_x + pt2_offset_x, pt2_y + pt2_offset_y)
        , bezier
        , bez_median
        , strk_wdth
        , line_stroke_color=line_stroke_color
        , line_stroke_opacity=line_stroke_opacity
        , start_end_flag=start_end_flag
        , arrow_stroke_dasharray=arrow_stroke_dasharray
        )
    

def mynote(dot, radius, interval, label, fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg, ns
           ):
    """
    Draw Single Note Dot
 
    dot: Tuple, (fret_number, string_number)
    radius: Number, dot radius in chord image
    interval: String, note interval from root.
        'h' appended to interval letter can be used for formatting:
        ('Rh' can be formatted in a different way from 'R')
    label: String, label inside dot
    fret0: Boolean, if true you can draw dots above nut
    centers_matrix: List of List, dots centers matrix
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
    dwg: Svgwrite object
    ns: Number, number of strings, is 6 for guitar

    return nothing
    """
    
    # if fret0 is enabled adjust (dot_x, dot_y) 
    if fret0: 
        dot_x = centers_matrix[dot[0]][abs(dot[1] - ns)][0]
        dot_y = centers_matrix[dot[0]][abs(dot[1] - ns)][1]      
    else:
        dot_x = centers_matrix[dot[0] - 1][abs(dot[1] - ns)][0]
        dot_y = centers_matrix[dot[0] - 1][abs(dot[1] - ns)][1]   

    # if dot is above nut
    if dot[0] == 0:
        # if interval.lower() in fret0_format:
        if interval.lower() in fret0_format:
            (
                dot_radius_scale, 
                dot_fill, 
                dot_fill_opacity, 
                dot_stroke, 
                dot_stroke_opacity, 
                dot_stroke_dasharray, 
                dot_stroke_width, 
                label_fill, 
                label_fill_opacity, 
                dot_labelfont_weight, 
                dot_labelfont_family, 
                dot_isquare, 
                dot_rotate 
            ) = fret0_format[interval.lower()]
        else:
            (
                dot_radius_scale, 
                dot_fill, 
                dot_fill_opacity, 
                dot_stroke, 
                dot_stroke_opacity, 
                dot_stroke_dasharray, 
                dot_stroke_width, 
                label_fill, 
                label_fill_opacity, 
                dot_labelfont_weight, 
                dot_labelfont_family, 
                dot_isquare, 
                dot_rotate 
            ) = fret0_format['*']
    
    else:   
        if interval.lower() in fretb_format:
            (
                dot_radius_scale, 
                dot_fill, 
                dot_fill_opacity, 
                dot_stroke, 
                dot_stroke_opacity, 
                dot_stroke_dasharray, 
                dot_stroke_width, 
                label_fill, 
                label_fill_opacity, 
                dot_labelfont_weight, 
                dot_labelfont_family, 
                dot_isquare, 
                dot_rotate 
            ) = fretb_format[interval.lower()]
        else:
            (
                dot_radius_scale, 
                dot_fill, 
                dot_fill_opacity, 
                dot_stroke, 
                dot_stroke_opacity, 
                dot_stroke_dasharray, 
                dot_stroke_width, 
                label_fill, 
                label_fill_opacity, 
                dot_labelfont_weight, 
                dot_labelfont_family, 
                dot_isquare, 
                dot_rotate 
            ) = fretb_format['*']
    
    # if dot_stroke_dasharray is set to keyword 'dashes' then all
    # dasharray calculation are automaticaly done
    if dot_stroke_dasharray == 'dashes':
        # calculate fretx_format tuple dot_stroke_dasharray from effective radius
        effective_radius = dot_radius_scale * radius
        stroke_dasharray_crcl =  str((effective_radius * 6.28)  / 20.00)     # dasharray for circles
        stroke_dasharray_rct =   str((effective_radius + 0.005) /  3.00)     # dasharray for rects
        if dot_isquare:
            dot_stroke_dasharray = stroke_dasharray_rct
        else:
            dot_stroke_dasharray = stroke_dasharray_crcl
    
    mydots.mydot(
        dwg, (dot_x, dot_y), label, 
        radius=              radius * dot_radius_scale,
        dotfill=             dot_fill,
        dotfill_opacity=     dot_fill_opacity,
        dotstroke=           dot_stroke, 
        dotstroke_opacity=   dot_stroke_opacity,
        dotstroke_dasharray= dot_stroke_dasharray, 
        dotstroke_width=     dot_stroke_width, 
        labelfill=           label_fill,
        labelfill_opacity=   label_fill_opacity,
        labelfont_weight=    dot_labelfont_weight, 
        labelfont_family=    dot_labelfont_family,
        square=              dot_isquare,
        sq_rotate=           dot_rotate
        )


def draw_dots(frets, intervals, dlabels, radius, fret0, first_fret, centers_matrix,
              fretb_format, fret0_format,
              dwg, ns
              ):
    """
    Draw Note Dots
 
    frets: List of strings, fret sequence
    intervals: List of strings, interval sequence.
        'h' appended to interval letter can be used for formatting:
        ('Rh' can be formatted in a different way from 'R')
    dlabels: List of strings, dot labels sequence
    radius: Number, dot radius in chord image
    fret0: Boolean, if true you can draw dots above nut    
    first_fret: Number, min fret number
    centers_matrix: List of List, dots centers matrix
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
    dwg: Svgwrite object
    ns: Number, number of strings, is 6 for guitar

    return nothing
    """
    
    # filter on frets (erase 'x'): ['x','3','2','0','1','0'] -> [None,'3','2','0','1','0']
    frets_fltrd = [fr if fr.isdigit() else None for fr in frets]
    for idx, currfrt in enumerate(frets_fltrd):
        # check if intervals[idx] exist
        try:
            interval = intervals[idx]
        except IndexError:
            # otherwise interval is ''
            interval = ''
        # check if dlabels[idx] exist
        try:
            label = dlabels[idx]
        except IndexError:
            # otherwise label is ''
            label = ''
        if currfrt:
            # if first_fret > 0 and new normalized fret is not negative or 0 then normalize fret number
            if (first_fret > 0): 
                # calculate shifted fret for candidate new normalized fret
                shifted_fret = int(currfrt) - (first_fret) + 1
                # if shifted_fret is > 0 then it can be the new normalized fret, else 0
                normfrt = shifted_fret if (shifted_fret > 0) else 0
            else:
                normfrt = int(currfrt)
            # draw a dot only if fret is > 0 or ( fret is = 0 but fret0 is enabled )
            # if (normfrt > 0) or (fret0 and label!='x'):
            if (normfrt > 0) or fret0:
                mynote(
                    (normfrt, ns - idx), radius, interval, label, fret0, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                )


def draw_scale_dots(strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, 
                    radius, fret0, first_fret, centers_matrix,
                    fretb_format, fret0_format,
                    dwg, ns
                    ):
    """
    Draw Scale Note Dots, reusing chord draw function draw_dots(). We think of a scale image
    as multiple chords joined together each chord is in a single fret
    
    strgs_frets_list: list of string lists (6 elements, one for every guitar String - frets positions)
        ie: [['5', '5', '5', '5', '5', '5'], ['x', '6', 'x', 'x', 'x', 'x'], ...]
    strgs_intervals_list: list of string lists (6 elements, one for every guitar String - intervals positions), optional
        ie: [['R', '4', 'b7', 'b3', '5', 'R'], ['x', 'b5', 'x', 'x', 'x', 'x'], ...]
    strgs_dlabels_list: list of string lists (6 elements, one for every guitar String - dlabels positions), optional
        ie: [['1', '1', '1', '1', '1', '1'], ['x', '2', 'x', 'x', 'x', 'x'], ...]
    footer: list of strings (6 elements, one for every guitar String - footers), optional
        ie: ['E', 'A', 'D', 'G', 'B', 'e']
    radius: Number, dot radius in chord image
    fret0: Boolean, if true you can draw dots above nut    
    first_fret: Number, min fret number
    centers_matrix: List of List, dots centers matrix
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
    dwg: Svgwrite object
    ns: Number, number of strings, is 6 for guitar

    return nothing
    """

    # compute len of first list element of strgs_frets_list. Since all 6
    # element must have same lenght that is global lenght of each element.
    # Moreover intervals and dlabels can be [] as they are optional but if 
    # they are not-null then their lenght must be equal to 
    # len_strg_frets (since strgs_frets_list is not optional)
    len_strg_frets = len(strgs_frets_list[0])
        
    '''
    now use global_utilities.traspose_fretb to traspose rows to columns 
    to get regular chords and use chords functions:
    so strgs_frets_list 
    [
          ['5', 'x', 'x', '8']
        , ['5', 'x', 'x', '8']
        , ['5', 'x', '7', '8']
        , ['5', 'x', '7', 'x']
        , ['5', '6', '7', 'x']
        , ['5', 'x', 'x', '8']
    ]
    become crds list
    [
          ['5', '5', '5', '5', '5', '5']
        , ['x', '6', 'x', 'x', 'x', 'x']
        , ['x', '7', '7', '7', 'x', 'x']
        , ['8', 'x', 'x', '8', '8', '8']
    ]
    
    and so strgs_intervals_list and strgs_dlabels_list
    '''
    crds = global_utilities.traspose_fretb(strgs_frets_list)
    intrvls = global_utilities.traspose_fretb(strgs_intervals_list)
    dlbls = global_utilities.traspose_fretb(strgs_dlabels_list)
    
    # reuse function draw_dots multiple time to draw the scale
    # treat each Fret as a single chord
    for n in range(len_strg_frets):
        # check if intrvls and dlbls exist, while crds must not be []
        act_intrvls = intrvls[n] if intrvls else []
        act_dlbls = dlbls[n] if dlbls else []
        draw_dots(crds[n], act_intrvls, act_dlbls,
                  radius, fret0, first_fret, centers_matrix,
                  fretb_format, fret0_format,
                  dwg, ns) 



if __name__ == "__main__":
    
    # testing this functions
    
    import svgwrite
    
    # -- common variables --

    ns = 6         # number of strings
    nf = 4         # number of frets
    radius = 20.0  # dot radius
    strk_wdth = 3  # line/dot tickness


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
                'black', '1.0', 'none', '3', 
                'white', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '0.5', 'none', '5', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 False, False)
        , '3': (1.0, 'lightsalmon', '1.0', 
                'black', '1.0', 'none', '5', 
                'black', '0.5', 'bold', 'Ubuntu Mono Legacy', 
                 False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '0.2', 
                'black', '1.0', 'dashes', '3', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', '3', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                True, False)
    }
    
    centers_matrix = [
          [(66.5, 41.5),  (116.5, 41.5),  (166.5, 41.5),  (216.5, 41.5),  (266.5, 41.5),  (316.5, 41.5)]
        , [(66.5, 106.5), (116.5, 106.5), (166.5, 106.5), (216.5, 106.5), (266.5, 106.5), (316.5, 106.5)]
        , [(66.5, 171.5), (116.5, 171.5), (166.5, 171.5), (216.5, 171.5), (266.5, 171.5), (316.5, 171.5)]
        , [(66.5, 236.5), (116.5, 236.5), (166.5, 236.5), (216.5, 236.5), (266.5, 236.5), (316.5, 236.5)]
        , [(66.5, 301.5), (116.5, 301.5), (166.5, 301.5), (216.5, 301.5), (266.5, 301.5), (316.5, 301.5)]
    ]
    
    transp_centers_matrix = [
          [(41.5, 291.5),  (41.5, 241.5),  (41.5, 191.5),  (41.5, 141.5),  (41.5, 91.5),  (41.5, 41.5)]
        , [(106.5, 291.5), (106.5, 241.5), (106.5, 191.5), (106.5, 141.5), (106.5, 91.5), (106.5, 41.5)]
        , [(171.5, 291.5), (171.5, 241.5), (171.5, 191.5), (171.5, 141.5), (171.5, 91.5), (171.5, 41.5)]
        , [(236.5, 291.5), (236.5, 241.5), (236.5, 191.5), (236.5, 141.5), (236.5, 91.5), (236.5, 41.5)]
        , [(301.5, 291.5), (301.5, 241.5), (301.5, 191.5), (301.5, 141.5), (301.5, 91.5), (301.5, 41.5)]
    ]

    centers_matrix_nofret0 = centers_matrix[1:]
    
    transp_centers_matrix_nofret0 = transp_centers_matrix[1:]

    bottom_labels_centers_vector = [
        (66.5, 364.875), (116.5, 364.875), (166.5, 364.875), (216.5, 364.875), (266.5, 364.875), (316.5, 364.875)
        ]

    transp_bottom_labels_centers_vector = [
        (364.875, 291.5), (364.875, 241.5), (364.875, 191.5), (364.875, 141.5), (364.875, 91.5), (364.875, 41.5)
        ]

    side_labels_centers_vector = [
        (28.25, 106.5), (28.25, 171.5), (28.25, 236.5), (28.25, 301.5)
        ]

    transp_side_labels_centers_vector = [
        (106.5, 329.75), (171.5, 329.75), (236.5, 329.75), (301.5, 329.75)
        ]
    
    # -- test fret0 chord --
    
    fret0 = True
    first_fret = 0
    fret_str_lst =      ['3', '3', 'x', '0', '1', '0']
    intrvl_str_lst =    ['3', 'R', 'x', '5', '3', 'R']
    bttm_lbls_str_lst = ['3', '3', 'x', 'x', '1', 'x']
    side_lbls_str_lst = [None, None, '3', None, None, None]
    
    dwg1 = svgwrite.Drawing(filename='../dirout/draw_dots_test_fret0.svg', size=(360 , 400), debug=True)
    
    actual_centers_matrix = centers_matrix
    
    draw_dots(fret_str_lst, intrvl_str_lst, intrvl_str_lst,
              radius, fret0, first_fret, actual_centers_matrix,
              fretb_format, fret0_format,
              dwg1, ns)
    mylabels.draw_labels(bttm_lbls_str_lst, (radius * 0.7),
                bottom_labels_centers_vector, dwg1,
                font_weight="bold", font_family="Ubuntu Mono")
    mylabels.draw_labels(side_lbls_str_lst, (radius * 0.5),
                side_labels_centers_vector, dwg1,
                font_weight="bold", font_family="Ubuntu Mono")
    
    # draw centers matrix
    for row in actual_centers_matrix:
        for point in row:
            dwg1.add(dwg1.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
    
    dwg1.save() 
    
    
    # -- test no fret0 chord --
    
    fret0 = False
    first_fret = 3
    fret_str_lst =      ['3', '5', '5', '4', '3', 'x']
    intrvl_str_lst =    ['R', '5', 'R', '3', '5', 'x']
    bttm_lbls_str_lst = ['1', '3', '4', '2', '1', 'x']
    side_lbls_str_lst = ['3', None, None, None, None, None]
    
    dwg2 = svgwrite.Drawing(filename='../dirout/draw_dots_test_nofret0.svg', size=(360 , 400), debug=True)
    
    actual_centers_matrix = centers_matrix_nofret0

    draw_dots(fret_str_lst, intrvl_str_lst, intrvl_str_lst,
              radius, fret0, first_fret, actual_centers_matrix,
              fretb_format, fret0_format,
              dwg2, ns)
    mylabels.draw_labels(bttm_lbls_str_lst, (radius * 0.7),
                bottom_labels_centers_vector, dwg2,
                font_weight="bold", font_family="Ubuntu Mono")
    mylabels.draw_labels(side_lbls_str_lst, (radius * 0.5),
                side_labels_centers_vector, dwg2,
                font_weight="bold", font_family="Ubuntu Mono")
    
    # draw centers matrix
    for row in actual_centers_matrix:
        for point in row:
            dwg2.add(dwg2.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
    
    dwg2.save()
    
    
    # -- test for arrows --
    
    fret0 = False
    first_fret = 1
    start_end_flag = 'se' # 'se', 's', 'e', ''
    bezier = True
    arrow_stroke_dasharray = None
    horiz = False
    
    dwg3 = svgwrite.Drawing(filename='../dirout/draw_dots_test_arrows.svg', size=(360 , 400), debug=True)
    
    mynote((1, 6) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((1, 2) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((4, 6) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((3, 2) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((2, 4) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((4, 1) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((3, 1) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )
    mynote((4, 3) , radius, 'R', '', fret0, centers_matrix,
           fretb_format, fret0_format,
           dwg3, ns
           )

    myarrow((1,6), (4,6), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'black', '0.5', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((3,2), (1,2), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'brown', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((1,6), (1,2), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'green', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((3,2), (4,6), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'red', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((1,6), (2,4), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'blue', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((1,2), (2,4), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'black', '0.5', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((4,6), (2,4), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'brown', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((3,2), (2,4), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'green', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((4,1), (3,1), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'blue', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)
    myarrow((4,1), (4,3), radius, fret0, first_fret, centers_matrix, horiz, strk_wdth, 
            'black', '0.5', start_end_flag, bezier, arrow_stroke_dasharray, dwg3, ns)

    # draw centers matrix
    for row in centers_matrix:
        for point in row:
            dwg3.add(dwg3.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
    
    dwg3.save()
    
    
    # -- test for transposed arrows --
    
    fret0 = False
    first_fret = 1
    start_end_flag = 'e' # 'se', 's', 'e', ''
    bezier = True
    arrow_stroke_dasharray = None
    horiz = True
    
    dwg7 = svgwrite.Drawing(filename='../dirout/draw_dots_test_arrows_transp.svg', size=(360 , 400), debug=True)
    
    mynote((1, 6) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((1, 2) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((4, 6) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((3, 2) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((2, 4) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((4, 1) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((3, 1) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )
    mynote((4, 3) , radius, 'R', '', fret0, transp_centers_matrix,
           fretb_format, fret0_format,
           dwg7, ns
           )

    myarrow((1,6), (4,6), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'black', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((3,2), (1,2), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'brown', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((1,6), (1,2), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'green', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((3,2), (4,6), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'red', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((1,6), (2,4), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'blue', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((1,2), (2,4), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'black', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((4,6), (2,4), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'brown', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((3,2), (2,4), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'green', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((4,1), (3,1), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'blue', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)
    myarrow((4,1), (4,3), radius, fret0, first_fret, transp_centers_matrix, horiz, strk_wdth, 
            'black', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg7, ns)

    # draw centers matrix
    for row in transp_centers_matrix:
        for point in row:
            dwg7.add(dwg7.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
    
    dwg7.save()
    

    # -- test for scales movable position --
    
    fret0 = False
    first_fret = 5
    horiz = False   
    start_end_flag = 'e'
    bezier = True
    arrow_stroke_dasharray = 'dashes'
    
    strgs_frets_list = [
          ['5', 'x', 'x', '8']
        , ['5', 'x', 'x', '8']
        , ['5', 'x', '7', '8']
        , ['5', 'x', '7', 'x']
        , ['5', '6', '7', 'x']
        , ['5', 'x', 'x', '8']
        ]
    strgs_intervals_list = [
          ['R', 'x', 'x', 'b3']
        , ['5', 'x', 'x', 'b7']
        , ['b3', 'x', '4', 'b5']
        , ['b7', 'x', 'R', 'x']
        , ['4', 'b5', '5', 'x']
        , ['R', 'x', 'x', 'b3']
        ]
    strgs_dlabels_list = [
          ['1', 'x', 'x', '4']
        , ['1', 'x', 'x', '4']
        , ['1', 'x', '3', '4']
        , ['1', 'x', '3', 'x']
        , ['1', '2', '3', 'x']
        , ['1', 'x', 'x', '4']
        ]
    
    footer = ['E', 'A', 'D', 'G', 'B', 'e']
    side_lbls_str_lst = ['5', None, None, None, None, None]
    
    dwg4 = svgwrite.Drawing(filename='../dirout/test_draw_scales_movable.svg', size=(400 , 400), debug=True)
    
    if horiz:
        actual_bottom_labels_centers_vector = transp_bottom_labels_centers_vector
        actual_side_labels_centers_vector = transp_side_labels_centers_vector
        if fret0:
            actual_centers_matrix = transp_centers_matrix
        else:
            actual_centers_matrix = transp_centers_matrix_nofret0
    else:
        actual_bottom_labels_centers_vector = bottom_labels_centers_vector
        actual_side_labels_centers_vector = side_labels_centers_vector         
        if fret0:
            actual_centers_matrix = centers_matrix
        else:
            actual_centers_matrix = centers_matrix_nofret0

    draw_scale_dots(strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, 
                        radius, fret0, first_fret, actual_centers_matrix,
                        fretb_format, fret0_format,
                        dwg4, ns
                        )
    
    mylabels.draw_labels(footer, (radius * 0.7),
                actual_bottom_labels_centers_vector, dwg4,
                font_weight="bold", font_family="Ubuntu Mono")
    
    mylabels.draw_labels(side_lbls_str_lst, (radius * 0.5),
                actual_side_labels_centers_vector, dwg4,
                font_weight="bold", font_family="Ubuntu Mono")
    
    myarrow((5,5), (7,5), radius, fret0, first_fret, actual_centers_matrix, horiz, strk_wdth, 
            'black', '1', start_end_flag, bezier, arrow_stroke_dasharray, dwg4, ns)
    
    # draw centers matrix
    for row in actual_centers_matrix:
        for point in row:
            dwg4.add(dwg4.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
    
    dwg4.save()    

    
# -- test for scales open position --
    
    fret0 = True
    first_fret = 1
    horiz = False
    
    strgs_frets_list = [
          ['0', '1', 'x', '3']
        , ['0', '1', 'x', '3']
        , ['0', 'x', '2', 'x']
        , ['0', 'x', '2', '3']
        , ['0', 'x', '2', '3']
        , ['0', '1', 'x', '3']
        ]
    strgs_intervals_list = [
          ['3', '4', 'x', '5']
        , ['7', 'R', 'x', '2']
        , ['5', 'x', '6', 'x']
        , ['2', 'x', '3', '4']
        , ['6', 'x', '7', 'R']
        , ['3', '4', 'x', '5']
        ]
    strgs_dlabels_list = [
          ['3', '4', 'x', '5']
        , ['7', 'R', 'x', '2']
        , ['5', 'x', '6', 'x']
        , ['2', 'x', '3', '4']
        , ['6', 'x', '7', 'R']
        , ['3', '4', 'x', '5']
        ]

    footer = ['E', 'A', 'D', 'G', 'B', 'e']
    side_lbls_str_lst = [None, None, '3', None, None, None]
    
    dwg5 = svgwrite.Drawing(filename='../dirout/test_draw_scales_open.svg', size=(400 , 400), debug=True)
    
    if horiz:
        actual_bottom_labels_centers_vector = transp_bottom_labels_centers_vector
        actual_side_labels_centers_vector = transp_side_labels_centers_vector
        if fret0:
            actual_centers_matrix = transp_centers_matrix
        else:
            actual_centers_matrix = transp_centers_matrix_nofret0
    else:
        actual_bottom_labels_centers_vector = bottom_labels_centers_vector
        actual_side_labels_centers_vector = side_labels_centers_vector         
        if fret0:
            actual_centers_matrix = centers_matrix
        else:
            actual_centers_matrix = centers_matrix_nofret0

    draw_scale_dots(strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, 
                        radius, fret0, first_fret, actual_centers_matrix,
                        fretb_format, fret0_format,
                        dwg5, ns
                        )
    
    mylabels.draw_labels(footer, (radius * 0.7),
                actual_bottom_labels_centers_vector, dwg5,
                font_weight="bold", font_family="Ubuntu Mono")
    
    mylabels.draw_labels(side_lbls_str_lst, (radius * 0.5),
                actual_side_labels_centers_vector, dwg5,
                font_weight="bold", font_family="Ubuntu Mono")
    
    # draw centers matrix
    for row in actual_centers_matrix:
        for point in row:
            dwg5.add(dwg5.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
    
    dwg5.save()
