
# local application imports
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

scale_label_isbottom = False            # if true scale main label goes at the bottom
scale_label_isleft = False                  # if true scale main label is left aligned otherwise is centered
enable_header = True                    # if True enable header labels
enable_dotlabels = True                 # if True enable dot labels
enable_footer = True                    # if True enable footer labels
enable_fretnum = True                   # if true enable side labels
nutline = True                          # if True draw nut line ticker
convert_flag = True                     # if true output also png file
font_weight = 'normal'                  # global font weight: [ 'normal' | 'bold' ]
font_family = 'Ubuntu Mono derivative FChords'             # global font family: ['Courier New' | 'Ubuntu Mono' | 
                                        # 'DejaVu Sans Mono' | 'Liberation Mono']

# --- appearance  parameters
scale_label_font_weight = None          # main scale label, font weight
scale_label_font_family = None          # main scale label, font family
scale_label_font_factor = 0.60          # main scale label, font size factor: default is 0.50
upper_labels_font_weight = None         # upper labels, font weight
upper_labels_font_family = None         # upper labels, font family   
upper_labels_font_factor = None         # upper labels, font size factor: default is 1.15
bottom_labels_font_weight = None        # bottom labels, font weight
bottom_labels_font_family = None        # bottom labels, font family      
bottom_labels_font_factor = 0.75        # bottom labels, font size factor: default is 0.80
side_labels_font_weight = None          # side labels, font weight
side_labels_font_family = None          # side labels, font family
side_labels_font_factor = 0.60          # side labels, font size factor  : default is 0.70
                       
# calculate fretx_format dot_stroke_width from lntk
slim_stroke_str = str(lntk * 1.00)
fair_stroke_str = str(lntk * 1.16)    
fat_stroke_str =  str(lntk * 1.66) 


# ---- arpeggios test --------------------------------


# --- html report parameters
report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
ncols = 2               # number of columns for the gallery
thumb_width = '400.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

# --- main parameters
dir_output = './dirout/arpeggios'      # output dir for images
horiz = True                           # if true chord is horizontal otherwise vertical
fret0 = False                          # if True you can draw dots above nut
padding = None                         # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable

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
             'black', '1.0', 'none', fair_stroke_str, 
             'white', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
    , 'r':  (0.9, 'lightgrey', '1.0', 
             'black', '1.0', 'none', fat_stroke_str, 
             'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
             True, False)
    , '3': (1.0, 'lightsalmon', '1.0', 
             'black', '1.0', 'none', fair_stroke_str, 
             'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
    , '5': (1.0, 'lightgreen', '1.0', 
             'black', '1.0', 'none', fair_stroke_str, 
             'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
    , 'b7':  (1.0, 'skyblue', '1.0', 
             'black', '1.0', 'none', fair_stroke_str, 
             'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
             False, False)
}

fret0_format = {
      '*': (1.0, 'white', '1.0', 
            'black', '1.0', 'dashes', fair_stroke_str, 
            'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
            False, False)
    , 'r': (0.9, 'lightgrey', '1.0', 
            'black', '1.0', 'dashes', fair_stroke_str, 
            'black', '1.0', 'bold', 'Ubuntu Mono derivative FChords', 
            True, False)
}

# arrows_format default
# -------------------------
# (
#   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
#  )
arrows_format = (lntk, 'black', '1.0', 'e', True, '')

input_arpegfile = '../scls_tests_files/arpeggios-list.txt'

# check if report has to be done
if report != 'only':
    (  process_scales_msg_str
     , svg_file_path_list
     , png_file_path_list) = scales2files.process_scales_file(
        input_arpegfile, 
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

print(process_scales_msg_str)
