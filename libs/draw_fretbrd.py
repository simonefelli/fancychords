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
draw_fretbrd: fretboard geometry and fretboard grid drawing.

get_basic_params() computes dot radius and fretboard sizes from a few
parameters (sd string distance, fd fret distance, ns strings, nf frets, ...).
get_crd_params() turns them into lists of points: grid lines vertices, the
centers_matrix with the center of every possible dot (centers_matrix[fret][string])
and the centers of upper, side and bottom labels. For horizontal chords
all points are rotated (rotate_shift_trasf) instead of computing a second
geometry. draw_fretbrd() draws grid lines and nut using those points.
"""


def shift_down_trasf(pt, delta):
    """
    Trasformation function for a point (x,y) -> (x,y+delta)
    shift down the point

    pt: Tuple, point to shift
    delta: shist amount

    return a tuple representing the new point
    """    
    return (pt[0], pt[1] + delta)


def rotate_shift_trasf(pt, orig, width):
    """
    Trasformation function for a point (x,y) -> (x',y')
    If chord is horiz then then rotate and shift

    pt: Tuple, point to rotate and shift
    orig: Tuple, pivot point for rotation
    width: Number, width of object canvas to rotate

    return a tuple representing the new point
    """    
    x, y = pt[0], pt[1]
    return (y - (orig[1] - orig[0]), width - x + (orig[0] + orig[1]))


def apply_trasf_matrix(matrix, dimens, cstm_trasf, pt_couple=False):
    """
    Apply cstm_trasf function to a matrix of points (or tuples of points)

    matrix: List, input matrix/vector 
    dimens: Number, matrix dimension (1 is a vector, 2 is a 2D matrix)
    cstm_trasf: Function that will be applied to matrix's points
    pt_couple: Boolean, if true matrix element is not a single point (a tuple)
               but a couple of points (tuple of tuple), [((x1, y1), (x2, v2)), (...]

    return a list representing the new matrix
    """
    if (dimens > 1):
        # return matrix initialization
        out_matrix = [[None for el in row] for row in matrix]
    else:
        # vector initialization
        out_matrix = [None for el in matrix]
    for id_row, row in enumerate(matrix):
        if (dimens > 1):
            for id_el, el in enumerate(row):
                if pt_couple:
                    out_matrix[id_row][id_el] = (cstm_trasf(el[0]), cstm_trasf(el[1]))
                else:
                    out_matrix[id_row][id_el] = cstm_trasf(el)
        else:
            if pt_couple:
                out_matrix[id_row] = (cstm_trasf(row[0]), cstm_trasf(row[1]))
            else:
                out_matrix[id_row] = cstm_trasf(row)
    return out_matrix


def get_basic_params(radius_factor, lntk, ns, nf, fd, sd,
                 fret0, enable_header, enable_footer, enable_barre, enable_fretnum):
    """
    Calculate basic parameters, mainly radius, ftbrd w/h and various offsets

    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41   
    lntk: Number, grid line tickness
    ns: Number, number of strings, is 6 for guitar
    nf: Number, number of frets, should be no more than 4 for chords
    fd: Number, fret distance (px)
    sd: Number, string distance (px), optimal ratio is fd/sd = 1.3
    fret0: Boolean, if true you can draw dots above nut
    enable_header: Boolean, if true enable header
    enable_footer: Boolean, if true enable footer
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels

    return a tuple: radius, (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), offset_forfret0,
                    offset_upper_labels, offset_forbarre, offset_side_labels, offset_bottom_labels
    
    ftbrd_w/h is the grid itself, ftbrd_box_w/h is the grid plus the room
    needed around it (dots above the nut, upper labels or barre arcs,
    footer labels, side fret numbers)
    """
    
    # ====== Computing Parameters ======
    
    radius = sd * radius_factor             # dot radius
    ftbrd_w = (sd * (ns - 1)) + lntk        # fretboard width
    ftbrd_h = (fd * nf) + lntk              # fretboard height
    offset_forfret0 = (fd / 2.00) + radius  # offset for fret0. Distance from fretboard edge to upper box edge
                                            # in case of fret0 dot is to be placed
    offset_upper_labels = offset_forfret0   # offset for upper labels. Distance from fretboard edge to upper box edge
                                            # in case upper labels are to be placed. this offset is not cumulative 
                                            # with offset_forfret0 (before it was (fd * 0.80))
    offset_forbarre = (fd * 0.60)           # offset for upper barre. Distance from fretboard edge to upper box edge
                                            # in case a barre is to be placed. this offset is not cumulative 
                                            # with offset_forfret0 or offset_upper_labels
    offset_bottom_labels = (fd * 0.75)      # offset for bottom labels. Distance from fretboard edge to box bottom edge
                                            # in case of bottom labels are to be placed

    # if enable_fretnum offset for side labels
    if enable_fretnum:
        # offset for side labels. Distance from fretboard left side edge to box edge
        offset_side_labels = radius + (sd * 0.50)
    else:
        offset_side_labels = radius

    # ftbrd_box_h = ftbrd_h + some offset 
    # offset for fret0 is the largest and includes all others
    # then comes offset for enable_header that includes also offset for barre
    # so is a if .. elif .. elif structure

    # fretboard box height (ftbrd_box_h)
    if fret0: 
        ftbrd_box_h = ftbrd_h + offset_forfret0
    # or if enable_header or enable_barre then offset to offset_upper_labels
    elif enable_header:
        ftbrd_box_h = ftbrd_h + offset_upper_labels
    # or if enable_barre then offset to offset_forbarre
    elif enable_barre:
        ftbrd_box_h = ftbrd_h + offset_forbarre
    else:
        ftbrd_box_h = ftbrd_h
    
    # if enable_footer offset to offset_bottom_labels
    if enable_footer: 
        ftbrd_box_h += offset_bottom_labels
    # fretboard box width (ftbrd_box_w)
    # should be exactly
    # ftbrd_box_w = ftbrd_w + radius - (lntk/2) + offset_side_labels
    # but to take into account for some edge circles stroke width 
    # we neglet (lntk/2)
    ftbrd_box_w = ftbrd_w + radius + offset_side_labels

    return (
        radius,
        (ftbrd_w, ftbrd_h),
        (ftbrd_box_w, ftbrd_box_h),
        offset_forfret0,
        offset_upper_labels,
        offset_forbarre,
        offset_side_labels,
        offset_bottom_labels        
        )


def get_crd_params(x_or, y_or, radius_factor, lntk, ns, nf, fd, sd,
                 fret0, enable_header, enable_footer,
                 horiz, enable_barre, enable_fretnum):
    """
    Calculate more complex chord parameters, mainly (x0, y0) and all the centers matrices

    x_or: Number, fretboard box origin (x)
    y_or: Number, fretboard box origin(y)
    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41
    lntk: Number, grid line tickness
    ns: Number, number of strings, is 6 for guitar
    nf: Number, number of frets, should be no more than 4 for chords
    fd: Number, fret distance (px)
    sd: Number, string distance (px), optimal ratio is fd/sd = 1.3
    fret0: Boolean, if true you can draw dots above nut
    enable_header: Boolean, if true enable header
    enable_footer: Boolean, if true enable footer
    horiz: Boolean, if true chord is horizontal otherwise vertical
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels

    return a tuple: radius, (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), 
                    horiz_lines_vertex, vertcl_lines_vertex, centers_matrix, 
                    upper_labels_centers_vector, side_labels_centers_vector, 
                    bottom_labels_centers_vector
    """
    
    # ====== Computing Parameters ======
    
    ll = lntk / 2 
    upper_labels_centers_vector = []        # list with upper label centers (x,y)
    side_labels_centers_vector = []         # list with side label centers (x,y)
    bottom_labels_centers_vector = []       # list with bottom label centers (x,y)
    # get basic Parameters
    (
        radius,
        (ftbrd_w, ftbrd_h),
        (ftbrd_box_w, ftbrd_box_h),
        offset_forfret0,
        offset_upper_labels,
        offset_forbarre,
        offset_side_labels,
        offset_bottom_labels         
    ) = get_basic_params(radius_factor, lntk, ns, nf, fd, sd,
                     fret0, enable_header, enable_footer,
                     enable_barre, enable_fretnum)    
    
    # fretboard origin (x), offset to x0 for dots on fretboard borders + side_labels
    x0 = x_or + offset_side_labels
    
    # offset for y0. fret0 is the largest and includes all others
    # then comes offset_upper_labels that includes also offset_forbarre
    # so is a if .. elif .. elif structure
    
    # fretboard origin (y), offset to y_or for dots on fret 0 
    if fret0: 
        y0 = y_or + offset_forfret0
    # or if enable_header then offset to y0 for labels (0, X) above nut
    elif enable_header:
        y0 = y_or + offset_upper_labels
    # or if enable_barre then offset y0 to offset_forbarre
    elif enable_barre:
        y0 = y_or + offset_forbarre
    else:
        y0 = y_or
    # for use in rotate_shift_trasf function as width. 
    # cannot use ftbrd_box_w as we invert it with ftbrd_box_h on rotation.
    trasf_width_param = ftbrd_box_w
    # list with line vertexs couples [( (startx, starty), (starty, starty) ), ...]
    # is a list of tuples of tuples
    horiz_lines_vertex =  [((x0, y0 + ll + (i * fd)), (x0 + ftbrd_w, y0 + ll + (i * fd))) for i in range(nf + 1)]
    vertcl_lines_vertex = [((x0 + ll + (j * sd), y0), (x0 + ll + (j * sd), y0 + ftbrd_h)) for j in range(ns)]
    # dot centers matrix initialize
    centers_matrix = [[(None, None) for col in range(ns)] for row in range(nf)]
    # dot centers matrix populate 
    for row in range(nf):
        for col in range(ns):
            centers_matrix[row][col] = (x0 + ll + (col * sd), y0 + ll + (fd / 2) + (row * fd))
    # dot side labels centers vector populate
    for row in centers_matrix:
        side_labels_centers_vector.append((row[0][0] - (offset_side_labels * 0.85), row[0][1]))
    # if footer is enabled then populate bottom_labels_centers_vector
    if enable_footer:
        bottom_labels_centers_vector = [(el[0], el[1] + (offset_bottom_labels * 1.30)) for el in centers_matrix[nf - 1]]   
    # if fret0 add centers for dots above nut to the centers_matrix
    if fret0: 
        centers_matrix.insert(0, [(el[0], el[1] - fd) for el in centers_matrix[0]])
    # if enable_header add centers in upper_labels_centers_vector for numbers (0, X) above nut
    if enable_header:
        if fret0:
            # if dots above nut then upper_labels_centers_vector points are above second row list points in centers_matrix 
            upper_labels_centers_vector = [(el[0], el[1] - (offset_upper_labels * 1.12)) for el in centers_matrix[1]]
        else:
            # otherwise upper_labels_centers_vector points are above first row list points in centers_matrix
            upper_labels_centers_vector = [(el[0], el[1] - (offset_upper_labels * 1.12)) for el in centers_matrix[0]]
    
    # ====== Rotate (if needed)  ======
    
    # custom version of rotate_shift_trasf function
    def cstm_trasf(pt):
        return rotate_shift_trasf(pt, (x_or, y_or), trasf_width_param)
    
    # if rotation then apply traformations to all used elements
    if horiz:
        horiz_lines_vertex = apply_trasf_matrix(horiz_lines_vertex, 1, cstm_trasf, pt_couple=True)
        vertcl_lines_vertex = apply_trasf_matrix(vertcl_lines_vertex, 1, cstm_trasf, pt_couple=True)
        (x0, y0) = cstm_trasf((x0, y0))
        ftbrd_w, ftbrd_h = ftbrd_h, ftbrd_w
        ftbrd_box_w, ftbrd_box_h = ftbrd_box_h, ftbrd_box_w   
        centers_matrix = apply_trasf_matrix(centers_matrix, 2, cstm_trasf)
        upper_labels_centers_vector = apply_trasf_matrix(upper_labels_centers_vector, 1, cstm_trasf)
        side_labels_centers_vector = apply_trasf_matrix(side_labels_centers_vector, 1, cstm_trasf)
        bottom_labels_centers_vector = apply_trasf_matrix(bottom_labels_centers_vector, 1, cstm_trasf)          
    
    # ====== Output params  ======    
    
    return (
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
        )
    
    
def draw_fretbrd(nut,
                 lntk,
                 dwg,
                 horiz_lines_vertex,
                 vertcl_lines_vertex,
                 centers_matrix,
                 x_or, y_or, ftbrd_box_w, ftbrd_box_h,
                 side_labels_centers_vector,
                 bottom_labels_centers_vector,
                 upper_labels_centers_vector,
                 enable_header=False,
                 enable_footer=False,
                 edge_debug=False
                 ):
    """
    Draw fretboard

    nut: Boolean, if true draw nut on fretboard
    lntk: Number, grid line tickness
    dwg: Svgwrite object
    horiz_lines_vertex: List of tuples of tuples, list with horizontal lines vertexs couples
    vertcl_lines_vertex: List of tuples of tuples, list with vertical lines vertexs couples
    centers_matrix: List of list, dot centers matrix    
    x_or: Number, fretboard box origin (x)
    y_or: Number, fretboard box origin(y)
    ftbrd_box_w: Number, fretboard box width
    ftbrd_box_h: Number, fretboard box height
    side_labels_centers_vector: List of tuples, side dots labels point centers vector
    bottom_labels_centers_vector: List of tuples, bottom dots labels point centers vector
    upper_labels_centers_vector: List of tuples, upper dots labels point centers vector
    edge_debug: Boolean, if true draw debug borders and debug dots

    return nothing
    """
    
    # fretboard horizontal lines
    for i, el in enumerate(horiz_lines_vertex):
        start_point = el[0]
        end_point =   el[1]
        # if nut, first line is thicker (lntk * X.Y)
        if (i == 0) and nut:
            dwg.add(
                dwg.line(
                    start=start_point,
                    end=end_point,
                    stroke="black",
                    stroke_width=(lntk * 3.8),
                    stroke_linecap="round"
                    )
                )
        else:
            dwg.add(
                dwg.line(
                    start=start_point,
                    end=end_point,
                    stroke="black",
                    stroke_width=lntk
                    )
                )
    # fretboard vertical lines, from 6th (ticker) to 1st string (thinner)
    # lntk_offset is offset for lntk to decrease at every string
    lntk_offset = lntk/6.5
    for idx, el in enumerate(vertcl_lines_vertex):
        start_point = el[0]
        end_point =   el[1]
        dwg.add(
            dwg.line(
                    start=start_point,
                    end=end_point,
                    stroke="black",
                    stroke_width=(lntk * 1.85) - (lntk_offset * idx)
                )
            )
    # id debug then draw fretboard box, centers matrix. nut and footer labels vectors
    if edge_debug:
        # draw centers matrix
        for row in centers_matrix:
            for point in row:
                dwg.add(dwg.circle(center=point, r=2, fill="red", stroke="red", stroke_width="0"))
        # draw fretboard box
        dwg.add(dwg.rect((x_or, y_or), (ftbrd_box_w, ftbrd_box_h), fill='none', stroke='red', stroke_width='1'))
        # draw side labels vector
        for point in side_labels_centers_vector:
            dwg.add(dwg.circle(center=point, r=2, fill="green", stroke="green", stroke_width="0"))
        # draw footer labels
        if enable_footer:
            for point in bottom_labels_centers_vector:
                dwg.add(dwg.circle(center=point, r=2, fill="purple", stroke="purple", stroke_width="0"))
        # draw upper labels        
        if enable_header:
            for point in upper_labels_centers_vector:
                dwg.add(dwg.circle(center=point, r=2, fill="blue", stroke="blue", stroke_width="0"))
                
        for point in horiz_lines_vertex:
            dwg.add(dwg.circle(center=point[0], r=2, fill="pink", stroke="pink", stroke_width="0"))
            dwg.add(dwg.circle(center=point[1], r=2, fill="pink", stroke="pink", stroke_width="0"))
            
        for point in vertcl_lines_vertex:
            dwg.add(dwg.circle(center=point[0], r=2, fill="yellow", stroke="yellow", stroke_width="0"))
            dwg.add(dwg.circle(center=point[1], r=2, fill="yellow", stroke="yellow", stroke_width="0"))            


if __name__ == "__main__":
    
    # testing this functions
    
    import svgwrite

    # --- internal parameters ---
    sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings, is 6 for guitar
    nf = 10                          # number of frets, should be no more than 4 for chords
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
    horiz = False           # if true chord is horizontal otherwise vertical
    enable_header = True   # if True enable header labels
    enable_footer = True    # if True enable footer labels
    enable_barre = True    # if true draw barre/s on chord
    enable_fretnum = True   # if true enable side labels
    nut = True              # if true draw nut on fretboard and leave space
                            # for numbers above nut
    fret0 = False           # if True you can draw dots above nut


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
    ) = get_crd_params(x_or, y_or, radius_factor, lntk, ns, nf, fd, sd,
                       fret0=fret0,
                       enable_header=enable_header,
                       enable_footer=enable_footer,
                       horiz=horiz,
                       enable_barre=enable_barre,
                       enable_fretnum=enable_fretnum)
    
    print(
        'get_crd_params() output\n-----------------------'
        '\n- radius: ' + str(radius),
        '\n- (x0, y0): ' + str((x0, y0)),
        '\n- (ftbrd_w, ftbrd_h): ' + str((ftbrd_w, ftbrd_h)),
        '\n- horiz_lines_vertex: ' + str(horiz_lines_vertex),
        '\n- vertcl_lines_vertex: ' + str(vertcl_lines_vertex),
        '\n- centers_matrix: ' + str(centers_matrix),
        '\n- upper_labels_centers_vector: ' + str(upper_labels_centers_vector),
        '\n- side_labels_centers_vector: ' + str(side_labels_centers_vector),
        '\n- bottom_labels_centers_vector: ' + str(bottom_labels_centers_vector)
        )
    
    dwg = svgwrite.Drawing(filename='../dirout/draw_fretboard_test.svg', size=(ftbrd_box_w + (2 * x_or) , ftbrd_box_h + (2 * y_or)), debug=debug)
    
    draw_fretbrd(nut, lntk, dwg,
                 horiz_lines_vertex,
                 vertcl_lines_vertex,
                 centers_matrix,
                 x_or, y_or,
                 ftbrd_box_w, ftbrd_box_h,
                 side_labels_centers_vector,
                 bottom_labels_centers_vector,
                 upper_labels_centers_vector,
                 enable_footer=enable_footer,
                 edge_debug=debug
                 )    

    dwg.save()
    