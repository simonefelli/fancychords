
# standard library imports
import os

# local application imports
from libs import draw_scales


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
    horiz = False                   # if true scale is horizontal otherwise vertical
    scale_label_isbottom = False    # if true scale main label goes at the bottom
    scale_label_isleft = False      # if true scale main label is left aligned otherwise is centered
    enable_header = True            # if True enable header labels
    enable_footer = True            # if True enable footer labels
    enable_fretnum = True           # if true enable side labels
    enable_dotlabels = True         # if True enable dot labels
    nutline = True                  # if True draw nut line ticker
    
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
                'white', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'none', '5', 
                'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                False, False)
        , '3': (1.0, 'lightsalmon', '1.0', 
                'black', '1.0', 'none', '5', 
                'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', '3', 
                'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', '3', 
                'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
                True, False)
    }

    upper_labels_font_weight = 'bold'   # upper labels, font weight
    upper_labels_font_family = 'Ubuntu Mono derivative FChords'   # upper labels, font family 
    upper_labels_font_factor = None   # upper labels, font size factor: default is 1.15       
    bottom_labels_font_weight = 'bold'  # bottom labels, font weight
    bottom_labels_font_family = 'Ubuntu Mono derivative FChords'  # bottom labels, font family 
    bottom_labels_font_factor = None  # bottom labels, font size factor: default is 1.00       
    side_labels_font_weight = 'bold'    # side labels, font weight
    side_labels_font_family = 'Ubuntu Mono derivative FChords'    # side labels, font family
    side_labels_font_factor = None    # side labels, font size factor  : default is 0.70

    if not os.path.isdir('./dirout/'): os.makedirs('./dirout/')
 
    # -- test for draw_scale movable position --
    
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


    scale_name = 'Am Blues Pentatonic Scale\nPosition 1, Blue Note Missing'
    horiz = True
    fret0 = True
    arrows = [
          ((1,6), (3,6))
        , ((2,5), (3,5))
        , ((0,2), (3,2))
        ]
    
    # arrows_format default
    # -------------------------
    # (
    #   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
    #  )
    arrows_format = (lntk, 'blue', '1.0', 'e', True, 'dashes')

    font_weight = 'normal'              # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono derivative FChords'       # global font family: ['Courier New' | 'Ubuntu Mono' |  'DejaVu Sans Mono' | 'Liberation Mono']
    fret0_format = {}                 # fret0_format, for fret0 dots
    fretb_format = {}                 # fretb_format, for fretboard dots    
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
    

    dwg3, (x0, y0), (ftbrd_w, ftbrd_h), (ftbrd_box_w, ftbrd_box_h), (image_w, image_h) = draw_scales.draw_scale(
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
    
    dwg3.saveas(filename='./dirout/test_draw_scale_movable.svg')