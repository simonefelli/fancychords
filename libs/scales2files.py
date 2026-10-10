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


# standard library imports
import os

# local application imports
from libs import scale_parser
from libs import helper_functions
from libs import draw_scales
from libs import convert_svg2png


def nice_scalesprint_options(tabslen, fretb_format, fret0_format, arrows_format, **kwargs):
    '''
    Pretty print options for process_scales_file() function
    
    tabslen: Integer, number of spaces as tabulature
    fretx_format: Dict for draw_dots tuples formats (see docs)
    arrows_format: Tuple, for draw_scale formats (see docs)
    kwargs: Sequence, other args to be pretty printed
    
    return pretty print string
    '''
    len_kwargs = len(kwargs)
    # for building like ('{:<37} {} {:<37} {} ... ').format('input_crdf', input_crdf, ... )
    # {":" format_spec} Padding and aligning strings
    # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
    # and XX is the width for specific value.
    format_header = '\n{:<' + str(tabslen) + '} {}'
    # '{:<37} {} {:<37} {} {:<37} {} ... ' repeated as number of args in kwargs
    format_str = format_header * len_kwargs
    format_list = []
    for myitem in kwargs.items():
        # ['input_way:', 'file', 'input_crds:', '../tests/misc_tests_files', 'dir_output:', ...]
        format_list.extend([myitem[0]+':', myitem[1]])
    msg_str = (format_str).format(*format_list)
    # print freatboard formats in option summary
    msg_str += '\n\nFreatboard Formats\n------------------'
    msg_str += '\nfretb_format'
    for fretformat in fretb_format:
        msg_str += '\n- ' + fretformat + ': ' + str(fretb_format[fretformat])
    msg_str += '\nfret0_format'
    for fretformat in fret0_format:
        msg_str += '\n- ' + fretformat + ': ' + str(fret0_format[fretformat])
    msg_str += '\narrows_format\n- ' + str(arrows_format)
    return msg_str


def scale_list_to_files(
        scl_list, 
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
        ):
    """
    Draw svg/png scales from scl_list outputs in dir_output

    scl_list: List of lists, [
                    [   error_in_scale
                      , error_message
                      , scale_name
                      , scale_filename
                      , subfolder
                      , strgs_frets_list
                      , strgs_intervals_list
                      , strgs_dlabels_list
                      , footer
                      , arrows 
                    ], ..
                ]
        each list element should not be null 
        
    ie:
    
    [
        [
          False
        , ''
        , 'Am Blues Scale
        , Position 2'
        , 'Am Blues ScalePos2'
        , './Blues_Scale/'
        , [['x', '8', 'x', '10', '11'], ...]
        , [['x', 'b3', 'x', '4', 'b5'], ...]
        , [['x', '1', 'x', '3', '4'], ...]
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , [((5, 2), (8, 2)), ((5, 4), (7, 4)), ((6, 5), (7, 5))]
        ], ...
    ]
        
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
    padding: Tuple, (pad lower_fret, pad higher_fret), None to disable
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
    convert_flag: Boolean, if true output also png file
    debug: Boolean, if true draw debug borders and debug dots

    return Tuple: useful msg_str, svg_file_path_list, png_file_path_list
    """
    
    header = 'Drawing SVG Scales\n=================='
    print('\n' + header)
    svg_msg_str = header
    scale_filenames_list = []
    svg_file_path_list = []
    png_file_path_list = []

    # scale = [
    #     error_in_scale
    #   , error_message
    #   , scale_name
    #   , scale_filename
    #   , subfolder
    #   , strgs_frets_list
    #   , strgs_intervals_list
    #   , strgs_dlabels_list
    #   , footer
    #   , arrows  
    # ]
    for scale in scl_list:
        scale_name = scale[2]
        scale_filename = scale[3]        
        subfolder = scale[4]        
        strgs_frets_list = scale[5]
        strgs_intervals_list = scale[6]
        strgs_dlabels_list = scale[7]
        footer = scale[8]
        arrows = scale[9]

        scale_filenames_list.append(scale_filename)
        # check if subfolder exist
        if subfolder:
            path_output = os.path.join(dir_output, subfolder)
        else:
            path_output = dir_output + '/'
        # if path_output does not exist then create it
        if not os.path.isdir(path_output): os.makedirs(path_output)
        print_label1 = "* " + scale_filename
        print_label2 = " --> "
        svg_file_path = os.path.normpath(path_output + scale_filename + ".svg")
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.
        body = '{:<20} {:6} {}'.format(print_label1, print_label2, svg_file_path)
        print(body)
        svg_msg_str += '\n' + body
        
        if padding and len(padding)==2:
            lower_fret, higher_fret = padding
            strgs_frets_list, strgs_intervals_list, strgs_dlabels_list = helper_functions.pad_scales(
                 strgs_frets_list, strgs_intervals_list, strgs_dlabels_list, lower_fret, higher_fret
                 )
        
        draw_scales.scale_to_file(scale_name, scale_filename, strgs_frets_list, 
            strgs_intervals_list, strgs_dlabels_list, footer, arrows, 
            path_output, horiz, enable_header, enable_dotlabels,
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
        svg_file_path_list.append(svg_file_path)

    svg_info_str = '>>> ' + str(len(svg_file_path_list))  + ' svg files processed <<<'
    print(svg_info_str)
    svg_msg_str += '\n' + svg_info_str
    msg_str = svg_msg_str
    
    # converting to png part
    if convert_flag:
        # convert_list = [('./dirout/Seventh/', './dirout/Seventh/png/'), ...]
        convert_list = []
        # os.walk returns a generator, that creates a tuple of values 
        # (current_path, directories in current_path, files in current_path).
        for oswalk_triplet in os.walk(dir_output):
            root_path = oswalk_triplet[0]
            # basename = last dir in root_path: ./dirout/Nine/png/ -> png
            root_dir = os.path.basename(root_path)
            # filter only svg files
            files = [elem for elem in oswalk_triplet[2] if elem.endswith('svg')]
            # avoid png dir scanning
            if files and (root_dir != 'png'):
                curr_dir_out = root_path + '/'
                png_path = os.path.join(root_path, 'png/')
                convert_list.append((curr_dir_out, png_path))
        convert_msg_str = ''
        header = "\nConverting SVG Scales to PNG\n============================"
        print(header)
        convert_msg_str += header
        for curr_dir_out, curr_png_path in convert_list:
            cmsg_str, png_fp_list = convert_svg2png.convert_svg2png(
                curr_dir_out, curr_png_path, scale_filenames_list
                )
            convert_msg_str += cmsg_str
            png_file_path_list += png_fp_list
    else:
        convert_msg_str = ''
    
    png_info_str = '>>> ' + str(len(png_file_path_list))  + ' png files processed <<<'
    print(png_info_str)
    convert_msg_str += '\n' + png_info_str
    
    msg_str += '\n' + convert_msg_str + '\n'
    
    # print msg_str
    return msg_str, svg_file_path_list, png_file_path_list


def process_scales_file(
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
       ):
    """
    Draw scales (output svg/png) defined in a chords file
    and save them in a dir_output

    input_sclf: Scales text file 
    dir_output: String, output dir for chord image
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
    padding: Tuple, (pad lower_fret, pad higher_fret), None to disable
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
    convert_flag: Boolean, if true output also png file
    debug: Boolean, if true draw debug borders and debug dots

    return Tuple: explicative message, svg_file_path_list, png_file_path_list
    """

    # useful lambda function to shorten Ternary Operator Assignment:
    # mylongnamedvar=mylongnamedvar if mylongnamedvar is not None else 'default'
    # turn into: 
    # mylongnamedvar=shortenop(mylongnamedvar)
    shortenop = lambda x: x if x is not None else 'default'

    # outputs a useful option summary for information
    option_summary = '\nScales Options Summary\n======================'
    option_summary += nice_scalesprint_options(
         37
        , fretb_format
        , fret0_format
        , arrows_format
        , input_scalesfile=input_scalesfile[0:50]+' ...' if len(input_scalesfile)>51 else input_scalesfile
        , dir_output=dir_output
        , horiz=horiz
        , enable_header=enable_header
        , enable_dotlabels=enable_dotlabels
        , enable_footer=enable_footer
        , enable_fretnum=enable_fretnum
        , lntk=lntk
        , nutline=nutline
        , fret0=fret0
        , padding=padding
        , font_weight=font_weight
        , font_family=font_family
        , convert_flag=convert_flag
        , scale_label_font_weight=shortenop(scale_label_font_weight)
        , scale_label_font_family=shortenop(scale_label_font_family)
        , scale_label_font_factor=shortenop(scale_label_font_factor)
        , scale_label_isbottom=shortenop(scale_label_isbottom)
        , scale_label_isleft=shortenop(scale_label_isleft)
        , upper_labels_font_weight=shortenop(upper_labels_font_weight)
        , upper_labels_font_family=shortenop(upper_labels_font_family)
        , upper_labels_font_factor=shortenop(upper_labels_font_factor)
        , bottom_labels_font_weight=shortenop(bottom_labels_font_weight)
        , bottom_labels_font_family=shortenop(bottom_labels_font_family)
        , bottom_labels_font_factor=shortenop(bottom_labels_font_factor)
        , side_labels_font_weight=shortenop(side_labels_font_weight)
        , side_labels_font_family=shortenop(side_labels_font_family)
        , side_labels_font_factor=shortenop(side_labels_font_factor)
        )
    print(option_summary)

    # os normalize dir
    dir_output = os.path.normpath(dir_output)
    
    # os normalize dirs and files paths
    input_sclf = os.path.normpath(input_scalesfile)
    

    # scl_list = [
    #   [   error_in_scale
    #     , error_message
    #     , scale_name
    #     , scale_filename
    #     , subfolder
    #     , strgs_frets_list
    #     , strgs_intervals_list
    #     , strgs_dlabels_list
    #     , footer
    #     , arrows 
    #   ], ..
    # ]
    
    # get_scales_list_from_file -> (scl_list, msg_str)

    scl_list, get_scales_msg_str = scale_parser.get_scales_list_from_file(input_sclf)
    
    # print some info
    info_msg_str = '\nscl_list_from_file (' + str(len(scl_list)) + \
          ' scales):\n==============================='
    for elem in scl_list:
        scale_name = elem[2]
        # root_note = elem[1]
        frets = elem[5]
        interv = elem[6]
        info_msg_str += '\n> ' + scale_name
        info_msg_str += '\n* frets'
        for elem in frets: info_msg_str += '\n  ' + str(elem)
        info_msg_str += '\n* interv'
        for elem in interv: info_msg_str += '\n  ' + str(elem)
    print(info_msg_str)
    
    info_msg_str += '\n'
    
    # main draw svg part

    (  scale_list_to_files_msg_str
     , svg_file_path_list
     , png_file_path_list) = scale_list_to_files(
        scl_list, 
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

    get_scales_msg_str += info_msg_str + '\n' + scale_list_to_files_msg_str
    
    return option_summary + '\n' + get_scales_msg_str, svg_file_path_list, png_file_path_list



if __name__ == "__main__":
    
    # testing process_chords function
    
    # local application imports
    from libs import htmlreport

    # --- internal parameters ---
    sd = 55.00                      # string distance, optimal ratio is fd/sd = 1.30 - 1.40
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings, is 6 for guitar
    nf = 4                          # number of frets, should be no more than 4 for chords
    debug = True                   # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.40                  # fret distance                                
    radius_factor = 22.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (22.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples                                 
    
    enable_header = True                    # if True enable header labels
    enable_dotlabels = True                 # if True enable dot labels
    enable_footer = True                    # if True enable footer labels
    enable_fretnum = True                   # if true enable side labels
    nutline = True                          # if True draw nut line ticker
    convert_flag = True                     # if true output also png file
    font_weight = 'normal'                  # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono Legacy'             # global font family: ['Courier New' | 'Ubuntu Mono' | 
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
    bottom_labels_font_factor = None        # bottom labels, font size factor: default is 0.80
    side_labels_font_weight = None          # side labels, font weight
    side_labels_font_family = None          # side labels, font family
    side_labels_font_factor = None          # side labels, font size factor  : default is 0.70
                           
    # calculate fretx_format dot_stroke_width from lntk
    slim_stroke_str = str(lntk * 1.00)
    fair_stroke_str = str(lntk * 1.16)
    fat_stroke_str =  str(lntk * 1.66)
    
    # arrows_format default
    # -------------------------
    # (
    #   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
    #  )
    arrows_format = (lntk, 'black', '1.0', 'e', True, '')


    # ---- small scales test -----------------------------------

    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    ncols = 2               # number of columns for the gallery
    thumb_width = '350.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

    # --- main parameters
    dir_output = '../dirout/small'                # output dir for images
    # dir_output = 'C:\\Users\\sfelli\\simo\\dev\\python\\py3\\pychords\\app\\dirout'
    horiz = False                           # if true chord is horizontal otherwise vertical
    scale_label_isbottom = False            # if true scale main label goes at the bottom
    scale_label_isleft = False              # if true scale main label is left aligned otherwise is centered
    fret0 = True                            # if True you can draw dots above nut
    padding = None                          # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable

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
                'black', '1.0', 'none', slim_stroke_str, 
                'white', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'none', fat_stroke_str,
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                False, False)
    }
    
    # input_scalesfile = 'C:/Users/sfelli/simo/dev/python/py3/pychords/app/tests/misc_tests_files/scale-list.txt'        # full path for chord list txt
    input_scalesfile = '../tests/scls_tests_files/scale-list.txt'
    
    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = process_scales_file(
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
    
    print(process_scales_msg_str)


    # ---- large scales test --------------------------------
    
    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    ncols = 1               # number of columns for the gallery
    thumb_width = '1100.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

    # --- main parameters
    dir_output = '../dirout/large'                # output dir for images
    # dir_output = 'C:\\Users\\sfelli\\simo\\dev\\python\\py3\\pychords\\app\\dirout'
    horiz = True                            # if true chord is horizontal otherwise vertical
    scale_label_isbottom = False            # if true scale main label goes at the bottom
    scale_label_isleft = False              # if true scale main label is left aligned otherwise is centered
    fret0 = True                            # if True you can draw dots above nut
    padding = None                          # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable

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
                 'white', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'r':  (0.9, 'lightgrey', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 True, False)
        , 'b3': (1.0, 'lightsalmon', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'b5': (1.0, 'lightgreen', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'b7':  (1.0, 'skyblue', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
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
    
    input_scalesfile = '../tests/scls_tests_files/scales-all-neck.txt'
    
    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = process_scales_file(
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
    
    print(process_scales_msg_str)
    
    
    # ---- arpeggios test --------------------------------
    
    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    ncols = 2               # number of columns for the gallery
    thumb_width = '400.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

    # --- main parameters
    dir_output = '../dirout/arpeggios' # output dir for images
    horiz = True                           # if true chord is horizontal otherwise vertical
    scale_label_isbottom = True            # if true scale main label goes at the bottom
    scale_label_isleft = True              # if true scale main label is left aligned otherwise is centered
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
                 'white', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'r':  (0.9, 'lightgrey', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 True, False)
        , '3': (1.0, 'lightsalmon', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , '5': (1.0, 'lightgreen', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'b7':  (1.0, 'skyblue', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
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
    

    input_arpegfile = '../tests/scls_tests_files/arpeggios-list.txt'
    
    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = process_scales_file(
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


    # ---- arpeggios pad test --------------------------------
    
    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    ncols = 1               # number of columns for the gallery
    thumb_width = '1000.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

    # --- main parameters
    dir_output = '../dirout/arpeggios_pad' # output dir for images
    horiz = True                           # if true chord is horizontal otherwise vertical
    scale_label_isbottom = True            # if true scale main label goes at the bottom
    scale_label_isleft = True              # if true scale main label is left aligned otherwise is centered
    fret0 = False                          # if True you can draw dots above nut
    padding = (0, 12)                      # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable

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
                 'white', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'r':  (0.9, 'lightgrey', '1.0', 
                 'black', '1.0', 'none', fat_stroke_str, 
                 'black', '1.0', 'bold', 'Ubuntu Mono Legacy', 
                 True, False)
        , '3': (1.0, 'lightsalmon', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , '5': (1.0, 'lightgreen', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
                 'black', '1.0', 'normal', 'Ubuntu Mono Legacy', 
                 False, False)
        , 'b7':  (1.0, 'skyblue', '1.0', 
                 'black', '1.0', 'none', fair_stroke_str, 
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
    

    input_arpegfile = '../tests/scls_tests_files/arpeggios-list.txt'
    
    # check if report has to be done
    if report != 'only':
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list) = process_scales_file(
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
