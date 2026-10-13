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


# standard library imports
import argparse
import sys

# local application imports
from libs import global_utilities


# defaults

# --- internal parameters ---
sd = 55.00                      # string distance, optimal ratio is fd/sd = 1.30 - 1.40
lntk = 3.00                     # default grid line tickness
#  --- derived internal parameters ---
fd = sd * 1.40                  # fret distance
radius_factor = 22.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                # as a guideline: radius_factor = (22.00/sd)
                                # general formula for radius is: radius = sd * radius_factor
                                # single dot adjustments can be achieved through dot_radius_scale
                                # in fretx_format tuples   

# calculate fretx_format dot_stroke_width from lntk
fair_stroke_str = str(lntk * 1.16)
fat_stroke_str =  str(lntk * 1.66)

# draw_dots tuples default formats
# --------------------------------
    # (
    #   dot_radius_scale, dot_fill, dot_fill_opacity, 
    #   dot_stroke, dot_stroke_opacity, dot_stroke_dasharray, dot_stroke_width, 
    #   label_fill, label_fill_opacity, dot_labelfont_weight, dot_labelfont_family, 
    #   dot_isquare, dot_rotate
    #  )

# if not set, dot_labelfont_weight and dot_labelfont_family default to
# global font weight and global font family

tpl_generic_format = (1.0, 'black', '1.0', 
                      'black', '1.0', 'none', fair_stroke_str, 
                      'white', '1.0', '', '', 
                      False, False)
tpl_fret0_format =   (1.0, 'white', '1.0', 
                      'black', '1.0', 'dashes',  fair_stroke_str, 
                      'black', '1.0', '', '', 
                      False, False)

tpl_generic_root_format = (1.0, 'lightgrey', '1.0', 
                           'black', '1.0', 'none', fat_stroke_str, 
                           'black', '1.0', '', '', 
                           False, False)
tpl_fret0_root_format =   (1.0, 'lightgrey', '1.0', 
                           'black', '1.0', 'dashes', fair_stroke_str, 
                           'black', '1.0', '', '', 
                           False, False)

# arrows_format default
# -------------------------
# (
#   line_stroke_width, line_stroke_color, line_stroke_opacity, start_end_flag, bezier, arrow_stroke_dasharray
#  )
arrows_format = (lntk, 'black', '1.0', 'e', True, '')


# default params dict
#--------------------
default_params = {

    # --- core internal parameters

      'lntk': lntk                        # grid line tickness
    , 'fd': fd                            # fret distance
    , 'sd': sd                            # string distance, optimal ratio is fd/sd = 1.3
                                          # image_w = (6.30*sd) + 43.0
                                          # image_h = (9.79*sd) + 43.0
    , 'ns': 6                             # number of strings, is 6 for guitar
    , 'nf': 4                             # number of frets
    , 'radius_factor': radius_factor      # sd factor to get global dot radius
    , 'x_or': 20.0                        # fretboard box origin offset (x)
    , 'y_or': 20.0                        # fretboard box origin offset (y)
    , 'debug': False                      # if true draw debug borders and debug dots
    # --- html report parameters
    , 'ncols': 4                          # number of columns for the gallery
    , 'thumb_width': '350.0px'            # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    
    # default params that can be set by cli and/or config_file
    
    , 'dir_output': './'                    # output dir for images
    , 'horiz': False                        # if true scale is horizontal otherwise vertical
    , 'scale_label_isbottom': False         # if true scale main label goes at the bottom
    , 'scale_label_isleft': False           # if true scale main label is left aligned otherwise is centered
    , 'enable_header': True                 # draw labels above fret zero
    , 'enable_dotlabels': True              # draw dot labels
    , 'enable_footer': False                # draw footer labels
    , 'enable_barre': True                  # draw barre
    , 'enable_fretnum': True                # draw reference fret number
    , 'nutline': True                       # draw nut line ticker
    , 'fret0': False                        # draw virtual dots above nut
    , 'root_is_different': False            # draw different dots for root note
    , 'font_family': global_utilities.DEFAULT_FONT_FAMILY   # global font family
    , 'font_weight': 'normal'               # global font weight
    , 'convert_flag': False                 # convert images to png files 
    , 'report': 'disable'                   # generate html report

    # default params that can be set by config_file only
    
    , 'padding': None                    # tuple (lower_fret, higher_fret) for padding scales with 'x', None to disable
    , 'scale_label_font_family': None    # main scale label font family: default is global font family
    , 'scale_label_font_weight': None    # main scale label font weight: default is global font weight
    , 'scale_label_font_factor': None    # main scale label font size factor: default is 0.80
    , 'upper_labels_font_family': None   # upper labels font family: default is global font family
    , 'upper_labels_font_weight': None   # upper labels font weight: default is global font weight
    , 'upper_labels_font_factor': None   # upper labels font factor: default is 1.15
    , 'bottom_labels_font_family': None  # bottom labels font family: default is global font family
    , 'bottom_labels_font_weight': None  # bottom labels font weight: default is global font weight
    , 'bottom_labels_font_factor': None  # bottom labels font factor: default is 1.00
    , 'side_labels_font_family': None    # side labels font family: default is global font family
    , 'side_labels_font_weight': None    # side labels font weight: default is global font weight
    , 'side_labels_font_factor': None    # side labels font factor: default is 0.90

    # draw_dots tuples formats:
    # (
    #   dot_radius_scale, dot_fill, dot_stroke, dot_stroke_dasharray, dot_stroke_width, label_fill,
    #   dot_labelfont_weight, dot_labelfont_family, dot_isquare, dot_rotate
    #  )
    # fretboard format
    , 'fretb_format': {
          '*': tpl_generic_format
        , 'r': tpl_generic_format
        }
    # fret0 format
    , 'fret0_format': {
          '*': tpl_fret0_format
        , 'r': tpl_fret0_format
        }
    # arrows format
    , 'arrows_format': arrows_format

}



if __name__ == "__main__":

    program_version = '0.8'
    program_author = 'Simone Felli'
    
    # parser declaration
    # all the optional arguments that are to be checked by check() function
    # must default to None for script to work, see param_check() function
    
    parser = argparse.ArgumentParser(
          description='Simple scales drawing program'
        , prog='fancyscales'        
        , epilog='Have fun playing guitar!'
        )

    # --- required arguments ---

    parser.add_argument(
        'input_sclf'
        , help='input scales file path'
        )  

    # --- optional arguments ---

    parser.add_argument(
        '-v', '--version'
        , action='version'
        , version='%(prog)s program by Simone Felli, version: ' + program_version
        )
    parser.add_argument(
        '-cf', '--config_file'
        , dest='json_file'
        , help='input config json file path'
        )
    parser.add_argument(
        '-o', '--output-dir'
        , action='store'
        , dest='dir_output'
        , default=None
        , help='output dir for images, default is \'' 
            + str(default_params['dir_output']) + '\''
        )
    parser.add_argument(
        '-ho', '--horizontal'
        , action="store_true"
        , dest='horiz'
        , default=None
        , help='draw scales horizontally, default is ' 
            + str(default_params['horiz'])
        )
    parser.add_argument(
        '-lb', '--label_bottom'
        , action="store_true"
        , dest='scale_label_isbottom'
        , default=None
        , help='main label goes at the bottom, default is ' 
            + str(default_params['scale_label_isbottom'])
        )
    parser.add_argument(
        '-nh', '--no-header'
        , action="store_false"
        , dest='enable_header'
        , default=None
        , help='do not draw labels above fret zero, ' \
            'labels above fret zero are enabled by default'
        )
    parser.add_argument(
        '-ndl', '--no-dotlabels'
        , action="store_false"
        , dest='enable_dotlabels'
        , default=None
        , help='do not draw dot labels, dot labels are enabled by default'
        )
    parser.add_argument(
        '-ft', '--footer'
        , action="store_true"
        , dest='enable_footer'
        , default=None
        , help='draw footer labels, default is ' 
            + str(default_params['enable_footer'])
        )
    parser.add_argument(
        '-nfn', '--no-fretnumb'
        , action="store_false"
        , dest='enable_fretnum'
        , default=None
        , help='do not draw reference fret number, reference fret number is enabled by default'
        )    
    parser.add_argument(
        '-nnl', '--no-nut-line'
        , action="store_false"
        , dest='nutline'
        , default=None
        , help='do not draw nut line ticker, nut line is ticker by default'
        )
    parser.add_argument(
        '-n', '--nut'
        , action="store_true"
        , dest='fret0'
        , default=None
        , help='draw virtual dots above nut, default is ' 
            + str(default_params['fret0'])
        )
    parser.add_argument(
        '-rd', '--root-diff'
        , action='store_true'
        , dest='root_is_different'
        , default=None
        , help='draw different dots for root note, default is ' 
            + str(default_params['root_is_different'])
        )
    parser.add_argument(
        '-ff', '--font-family'
        , action='store'
        , dest='font_family'
        , default=None
        , choices=global_utilities.FONT_FAMILIES
        , help='global font family: [\'' + '\'|\''.join(global_utilities.FONT_FAMILIES)
               + '\'], default is \'' 
               + str(default_params['font_family']) + '\''
        )    
    parser.add_argument(
        '-fw', '--font-weight'
        , action='store'
        , dest='font_weight'
        , default=None
        , choices=['normal', 'bold']
        , help='global font weight: [\'normal\'|\'bold\'], default is \'' 
            + str(default_params['font_weight']) + '\''
        )
    parser.add_argument(
        '-c', '--convert'
        , action="store_true"
        , dest='convert_flag'
        , default=None
        , help='convert images to png files, default is ' 
            + str(default_params['convert_flag'])
        )
    parser.add_argument(
          '-r', '--report'
        , action='store'
        , dest='report'
        , default=None
        , choices=['only', 'enable', 'disable']
        , help='generate html report (\'enable\'/\'disable\') if \'only\' generate ' \
               'report but do not draw scales, default is \'' 
                + str(default_params['report']) + '\''
        )


    # -- main call of the parser --

    try:
        


        args = parser.parse_args()
        
        '''

        # for testing fancyscales
        args = parser.parse_args(
            [  
               './tests/scls_tests_files/scale-list.txt'
             , '-o', './dirout/'
             , '-r', 'enable'
             , '-rd'
             , '-c'
             , '-cf', './tests/json_cfg_tests_files/default_scales_config.json'
             ]
            )

        '''
        
        if args:
            
            # input file was used to input scale/s
            input_sclf = args.input_sclf
            
            db_dict_jdump = {}
            
            # if a json config file was passed as argument
            if args.json_file:
                # load its content in db_dict_jdump
                import json
                json_file = args.json_file
                with open(json_file, 'r', encoding='utf-8') as jsonfile:
                    db_dict_jdump = json.load(jsonfile)
                    # add missing parameters if any (see fill_jdump function: take the json config file 
                    # db_dict_jdump and check if there are missing parameters that can be calculated 
                    # from others with known formulas, if so db_dict_jdump is modified in place with 
                    # missing parameters added)
                    global_utilities.fill_jdump(db_dict_jdump, 1.40, 22.00, None)
        
        # Get all the variables using param_check() function
        # as this function applies precedence logic: check if a parameter of fancyscales is set 
        # by cli, by config file or is just as default. This logic applies: cli has highest precedence, 
        # then comes json config file and at last default. Return a Tuple:
        # - param value (type varies) set by precedence logic
        # - boolean, param is as default or not
        
        # params that can be set by cli and/or config_file
        dir_output = global_utilities.param_check(
            db_dict_jdump, args.dir_output, 
            'dir_output', 'i/o', 
            default_params)[0]
        horiz = global_utilities.param_check(
            db_dict_jdump, args.horiz, 
            'horiz', 'flags', 
            default_params)[0]
        scale_label_isbottom = global_utilities.param_check(
            db_dict_jdump, args.scale_label_isbottom, 
            'scale_label_isbottom', 'flags', 
            default_params)[0]
        enable_header = global_utilities.param_check(
            db_dict_jdump, args.enable_header, 
            'enable_header', 'flags', 
            default_params)[0]
        enable_dotlabels = global_utilities.param_check(
            db_dict_jdump, args.enable_dotlabels, 
            'enable_dotlabels', 'flags', 
            default_params)[0]
        enable_footer = global_utilities.param_check(
            db_dict_jdump, args.enable_footer, 
            'enable_footer', 'flags', 
            default_params)[0]
        enable_fretnum = global_utilities.param_check(
            db_dict_jdump, args.enable_fretnum, 
            'enable_fretnum', 'flags', 
            default_params)[0]
        nutline = global_utilities.param_check(
            db_dict_jdump, args.nutline, 
            'nutline', 'flags', 
            default_params)[0]
        fret0 = global_utilities.param_check(
            db_dict_jdump, args.fret0, 
            'fret0', 'flags', 
            default_params)[0]
        root_is_different = global_utilities.param_check(
            db_dict_jdump, args.root_is_different, 
            'root_is_different', 'flags', 
            default_params)[0]      
        font_weight = global_utilities.param_check(
            db_dict_jdump, args.font_weight, 
            'font_weight', 'generic_formats', 
            default_params)[0]
        font_family = global_utilities.param_check(
            db_dict_jdump, args.font_family, 
            'font_family', 'generic_formats', 
            default_params)[0]
        convert_flag = global_utilities.param_check(
            db_dict_jdump, args.convert_flag, 
            'convert_flag', 'flags', 
            default_params)[0]
        report = global_utilities.param_check(
            db_dict_jdump, args.report, 
            'report', 'flags', 
            default_params)[0]

        # params that can be set by config_file only
        scale_label_font_weight = global_utilities.param_check(
            db_dict_jdump, None, 
            'scale_label_font_weight', 'generic_formats', 
            default_params)[0]
        scale_label_font_family = global_utilities.param_check(
            db_dict_jdump, None, 
            'scale_label_font_family', 'generic_formats', 
            default_params)[0]
        scale_label_font_factor = global_utilities.param_check(
            db_dict_jdump, None, 
            'scale_label_font_factor', 'generic_formats', 
            default_params)[0]
        scale_label_isleft = global_utilities.param_check(
            db_dict_jdump, None, 
            'scale_label_isleft', 'flags', 
            default_params)[0]
        upper_labels_font_weight = global_utilities.param_check(
            db_dict_jdump, None, 
            'upper_labels_font_weight', 'generic_formats', 
            default_params)[0]
        upper_labels_font_family = global_utilities.param_check(
            db_dict_jdump, None, 
            'upper_labels_font_family', 'generic_formats', 
            default_params)[0]
        upper_labels_font_factor = global_utilities.param_check(
            db_dict_jdump, None, 
            'upper_labels_font_factor', 'generic_formats', 
            default_params)[0]
        bottom_labels_font_weight = global_utilities.param_check(
            db_dict_jdump, None, 
            'bottom_labels_font_weight', 'generic_formats', 
            default_params)[0]
        bottom_labels_font_family = global_utilities.param_check(
            db_dict_jdump, None, 
            'bottom_labels_font_family', 'generic_formats', 
            default_params)[0]
        bottom_labels_font_factor = global_utilities.param_check(
            db_dict_jdump, None, 
            'bottom_labels_font_factor', 'generic_formats', 
            default_params)[0]
        side_labels_font_weight = global_utilities.param_check(
            db_dict_jdump, None, 
            'side_labels_font_weight', 'generic_formats', 
            default_params)[0]
        side_labels_font_family = global_utilities.param_check(
            db_dict_jdump, None, 
            'side_labels_font_family', 'generic_formats', 
            default_params)[0]
        side_labels_font_factor = global_utilities.param_check(
            db_dict_jdump, None, 
            'side_labels_font_factor', 'generic_formats', 
            default_params)[0]
        fretb_format, fretb_asdefault = global_utilities.param_check(
            db_dict_jdump, None, 
            'fretb_format', 'generic_formats', 
            default_params)
        fret0_format, fret0_asdefault = global_utilities.param_check(
            db_dict_jdump, None, 
            'fret0_format', 'generic_formats', 
            default_params)
        arrows_format, arrows_asdefault = global_utilities.param_check(
            db_dict_jdump, None, 
            'arrows_format', 'generic_formats', 
            default_params)
        padding = global_utilities.param_check(
            db_dict_jdump, None, 
            'padding', 'parameters', 
            default_params)[0]
        lntk = global_utilities.param_check(
            db_dict_jdump, None, 
            'lntk', 'parameters', 
            default_params)[0]
        radius_factor = global_utilities.param_check(
            db_dict_jdump, None, 
            'radius_factor', 'parameters', 
            default_params)[0]
        ncols = global_utilities.param_check(
            db_dict_jdump, None, 
            'ncols', 'parameters', 
            default_params)[0]
        thumb_width = global_utilities.param_check(
            db_dict_jdump, None, 
            'thumb_width', 'parameters', 
            default_params)[0]        
        x_or = global_utilities.param_check(
            db_dict_jdump, None, 
            'x_or', 'parameters', 
            default_params)[0]
        y_or = global_utilities.param_check(
            db_dict_jdump, None, 
            'y_or', 'parameters', 
            default_params)[0]
        ns = global_utilities.param_check(
            db_dict_jdump, None, 
            'ns', 'parameters', 
            default_params)[0]
        nf = global_utilities.param_check(
            db_dict_jdump, None, 
            'nf', 'parameters', 
            default_params)[0]
        fd = global_utilities.param_check(
            db_dict_jdump, None, 
            'fd', 'parameters', 
            default_params)[0]
        sd = global_utilities.param_check(
            db_dict_jdump, None, 
            'sd', 'parameters', 
            default_params)[0]
        debug = global_utilities.param_check(
            db_dict_jdump, None, 
            'debug', 'flags', 
            default_params)[0] 
        

        # --- actual main work
        
        app_msg_str = '\nGlobal Options\n=============='

        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.
        app_msg_str += ('{:<22} {} {:<22} {} {:<22} {} {:<22} {} {:<22} {}').format(
            '\ninput scale/s file:', input_sclf,
            '\nconfig file:', str(args.json_file),            
            '\nroot is different:', root_is_different,
            '\nreport:', report,
            '\nconvert flag:', convert_flag
            )
        
        print(app_msg_str)
        
        
        # main functions call
        
        if report != 'only':
            
            # if root_is_different and also fretb and fret0
            # are as default then we need to change them
            if root_is_different:
                if fretb_asdefault:
                    fretb_format = {
                          '*': tpl_generic_format
                        , 'r': tpl_generic_root_format
                    }
                if fret0_asdefault:
                    fret0_format = {
                          '*': tpl_fret0_format
                        , 'r': tpl_fret0_root_format
                    }
            
            
            # import function to draw/output scales
            from libs import scales2files
            
            (  process_scales_msg_str
             , svg_file_path_list
             , png_file_path_list) = scales2files.process_scales_file(
                input_sclf, 
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

            app_msg_str += '\n' + process_scales_msg_str

        if report != 'disable':

            # local libraries imports
            from libs import htmlreport 

            file_exts = (".svg", ".png")
            app_msg_str += htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)


    # any error ends the program with a short message on stderr and exit
    # status 1, so that scripts calling fancyscales can tell a failed run
    # from a good one (before, the error was printed on stdout with status 0)
    except Exception as e:
        print('fancyscales error: ' + str(e), file=sys.stderr)
        sys.exit(1)
