
# standard library imports
import os

# local application imports
from libs import draw_scales

if __name__ == "__main__":
    
    # testing this functions

    # --- internal parameters ---
    
    sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings
    nf = 4                          # number of frets    
    debug = True                    # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.50                  # fret distance                                
    radius_factor = 20.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples
                                    
    dir_output = './dirout/'          # output dir for scale image
    scale_label_isbottom = False      # if true scale main label goes at the bottom
    scale_label_isleft = False        # if true scale main label is left aligned otherwise is centered
    enable_header = True              # if True enable header labels
    enable_dotlabels = True           # if True enable dot labels     
    enable_footer = True              # if True enable footer labels
    enable_fretnum = True             # if true enable side labels
    nutline = True                    # if True draw nut line ticker   
    font_weight = 'normal'            # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono Legacy'       # global font family: ['Courier New' | 'Ubuntu Mono' |  'DejaVu Sans Mono' | 'Liberation Mono']
    fret0_format = {}                 # fret0_format, for fret0 dots
    fretb_format = {}                 # fretb_format, for fretboard dots
    arrows_format = ()    
    scale_label_font_weight = None    # main chord label, font weight
    scale_label_font_family = None    # main chord label, font family
    scale_label_font_factor = None    # main scale label, font size factor: default is 0.50
    upper_labels_font_weight = None   # upper labels, font weight
    upper_labels_font_family = None   # upper labels, font family   
    upper_labels_font_factor = None   # upper labels, font size factor: default is 1.15
    bottom_labels_font_weight = None  # bottom labels, font weight
    bottom_labels_font_family = None  # bottom labels, font family      
    bottom_labels_font_factor = None  # bottom labels, font size factor: default is 1.00
    side_labels_font_weight = None    # side labels, font weight
    side_labels_font_family = None    # side labels, font family
    side_labels_font_factor = None    # side labels, font size factor  : default is 0.70

    if not os.path.isdir(dir_output): os.makedirs(dir_output)

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
    
    draw_scales.scale_to_file(
          'Vertical Scale\nTwo line Label Exceed Horiz', 'vert_test_1'
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
    
    draw_scales.scale_to_file(
          'Vertical Scale\nTwo line Label', 'vert_test_2'
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

    draw_scales.scale_to_file(
          'Vertical Scale One line Ex.', 'vert_test_3'
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
    
    draw_scales.scale_to_file(
          'Vertical Scale One Line H', 'vert_test_4'
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



    fret0 = False
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
    
    draw_scales.scale_to_file(
          'Horizontal Scale\nTwo line Label Exceed Horizontal Width XXy', 'horiz_test_1'
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
    
    draw_scales.scale_to_file(
          'Horizontal Scale\nTwo Lines Small Width', 'horiz_test_2'
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

    draw_scales.scale_to_file(
          'Horizontal Scale. One line Label Large WidthX', 'horiz_test_3'
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
    
    draw_scales.scale_to_file(
          'Horizontal One line Label', 'horiz_test_4'
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
