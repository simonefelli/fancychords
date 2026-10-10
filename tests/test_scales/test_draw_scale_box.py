
# standard library imports
import os

# third party imports
import svgwrite

# local application imports
from libs import draw_scales
from libs import draw_fretbrd


if __name__ == "__main__":
    
    # testing this functions

    ns = 6         # number of strings
    nf = 4         # number of frets
    
    sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    debug = True                    # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.50                  # fret distance                                
    radius_factor = 20.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples   
    
    # --- functions parameters ---
    horiz = False           # if true scale is horizontal otherwise vertical
    enable_header = True   # if True enable header labels
    enable_footer = True    # if True enable footer labels
    enable_barre = False    # if true draw barre/s on scale
    enable_fretnum = True   # if true enable side labels
    enable_dotlabels = True         # if True enable dot labels
    nutline = True                  # if True draw nut line ticker
    edge_debug = True  
    
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
                'black', '1.0', 'none', '5', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                False, False)
        , '3': (1.0, 'lightsalmon', '1.0', 
                'black', '1.0', 'none', '5', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', '3', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', '3', 
                'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                True, False)
    }

    centers_matrix = [
          [(70.0, 44),  (120.0, 44),  (170.0, 44),  (220.0, 44),  (270.0, 44),  (320.0, 44)]
        , [(70.0, 109), (120.0, 109), (170.0, 109), (220.0, 109), (270.0, 109), (320.0, 109)]
        , [(70.0, 174), (120.0, 174), (170.0, 174), (220.0, 174), (270.0, 174), (320.0, 174)]
        , [(70.0, 239), (120.0, 239), (170.0, 239), (220.0, 239), (270.0, 239), (320.0, 239)]
        , [(70.0, 304), (120.0, 304), (170.0, 304), (220.0, 304), (270.0, 304), (320.0, 304)]
        ]
    
    bottom_labels_centers_vector = [
        (70.0, 352.25), (120.0, 352.25), (170.0, 352.25), (220.0, 352.25), (270.0, 352.25), (320.0, 352.25)
        ]
    
    side_labels_centers_vector = [
        (32.0, 109), (32.0, 174), (32.0, 239), (32.0, 304)
        ]

    upper_labels_font_weight = 'bold'   # upper labels, font weight
    upper_labels_font_family = 'Ubuntu Mono Legacy'   # upper labels, font family 
    upper_labels_font_factor = 1.15   # upper labels, font size factor: default is 1.15       
    bottom_labels_font_weight = 'bold'  # bottom labels, font weight
    bottom_labels_font_family = 'Ubuntu Mono Legacy'  # bottom labels, font family 
    bottom_labels_font_factor = 1.00  # bottom labels, font size factor: default is 1.00       
    side_labels_font_weight = 'bold'    # side labels, font weight
    side_labels_font_family = 'Ubuntu Mono Legacy'    # side labels, font family
    side_labels_font_factor = 0.70    # side labels, font size factor  : default is 0.70

    if not os.path.isdir('./dirout/'): os.makedirs('./dirout/')


    # -- test for draw_scale_box movable position --

    fret0 = False
    horiz = False
    
    # arrows_format default
    # -------------------------
    # (
    #   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
    #  )
    arrows_format = (lntk, 'black', '1.0', 'e', True, 'dashes')

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
    arrows = [
          ((5,2), (8,2))
        , ((5,4), (7,4))
        , ((6,5), (7,5))
        ]

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
                       fret0=fret0,
                       enable_header=enable_header,
                       enable_footer=enable_footer,
                       horiz=horiz,
                       enable_barre=enable_barre,
                       enable_fretnum=enable_fretnum)

    ftbrd_box_wh = (ftbrd_box_w, ftbrd_box_h)

    dwg1 = svgwrite.Drawing(filename='./dirout/test_draw_scale_box_movable.svg', size=(450 , 450), debug=True)

    draw_scales.draw_scale_box(
        strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, footer, arrows,
        radius, centers_matrix,
        upper_labels_centers_vector, bottom_labels_centers_vector,
        side_labels_centers_vector, horiz_lines_vertex, vertcl_lines_vertex,
        ftbrd_box_wh, dwg1, nutline, fret0, enable_header, enable_dotlabels,
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
        )
    
    dwg1.save() 


    # -- test for draw_scale_box open position --
    
    fret0 = True
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
    arrows = []       
    
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
                       fret0=fret0,
                       enable_header=enable_header,
                       enable_footer=enable_footer,
                       horiz=horiz,
                       enable_barre=enable_barre,
                       enable_fretnum=enable_fretnum)

    ftbrd_box_wh = (ftbrd_box_w, ftbrd_box_h)

    dwg2 = svgwrite.Drawing(filename='./dirout/test_draw_scale_box_open.svg', size=(450 , 450), debug=True)

    draw_scales.draw_scale_box(
        strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, footer, arrows,
        radius, centers_matrix,
        upper_labels_centers_vector, bottom_labels_centers_vector,
        side_labels_centers_vector, horiz_lines_vertex, vertcl_lines_vertex,
        ftbrd_box_wh, dwg2, nutline, fret0, enable_header, enable_dotlabels,
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
        )
    
    dwg2.save()
