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
fancychords: command line program that draws guitar chord diagrams as svg
(and optionally png) images, plus an optional html gallery report.

Quick examples
--------------
    one chord from the command line (only name and frets are mandatory):
        python3 fancychords.py --cli_in="C Major|x,3,2,0,1,0"

    many chords from the command line, separated by ';':
        python3 fancychords.py --cli_in="C|x,3,2,0,1,0;G|3,2,0,0,0,3"

    many chords from a tab separated text file, with png and html report:
        python3 fancychords.py --file_in=./chords.txt -o ./out -c -r enable

Single chord fields (in this order, '|' separated on cli, tab separated in files)
-----------------------------------------------------------------------------------
    chord_name | frets | fingers | intervals | dlabels | footer | subfolder
    Use '%' to skip an optional field and still give the following ones.

How a run works
---------------
    1. argparse reads the command line options (this file)
    2. if -cf is given, the json config file is loaded (this file)
    3. every parameter gets its final value with this precedence:
           command line  >  json config file  >  default_params (below)
       (see global_utilities.param_check)
    4. libs/chords2files.process_chords() does the real work:
           chord_parser    -> read and validate chords
           draw_chords     -> draw one svg file per chord (svgwrite)
           convert_svg2png -> optional png conversion (cairosvg)
    5. libs/htmlreport.generate_htmlreport() builds the optional html gallery

Exit status is 0 on success and 1 on error (message printed on stderr).
"""

# standard library imports
import argparse     # command line options parsing
import sys          # stderr and exit status

# local application imports
# note: other libs (chords2files, htmlreport, json) are imported later,
# only when they are really needed, so that '--help' and '--version'
# work even if third party libs (svgwrite, cairosvg) are not installed
from libs import global_utilities


# =============================================================================
# defaults
# =============================================================================
# All sizes are in svg user units (pixels when the svg is shown at 100%).
# Image size grows with sd (string distance), as a rule of thumb:
#     image_w = (6.30 * sd) + 43.0
#     image_h = (9.79 * sd) + 43.0

# --- factors used to derive some parameters from others ---
# they are also used by global_utilities.fill_jdump() to calculate the
# same parameters when they are missing in a json config file, so the
# image proportions are the same whichever way the values are given
FD_FACTOR = 1.30                # fd = sd * FD_FACTOR
RADIUS_FACTOR_K = 20.00         # radius_factor = RADIUS_FACTOR_K / sd
BARRE_FACTOR = 1.10             # barre_strk_wdth = lntk * BARRE_FACTOR

# --- internal parameters ---
sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
lntk = 3.00                     # default grid line tickness
#  --- derived internal parameters ---
fd = sd * FD_FACTOR             # fret distance
radius_factor = RADIUS_FACTOR_K / sd  # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                # as a guideline: radius_factor = (20.00/sd)
                                # general formula for radius is: radius = sd * radius_factor
                                # single dot adjustments can be achieved through dot_radius_scale
                                # in fretx_format tuples   
barre_strk_wdth = BARRE_FACTOR * lntk  # barre arc tickness

# calculate fretx_format dot_stroke_width from lntk
# (svg wants strings for these attributes, so they are stored as str)
slim_stroke_str = str(lntk * 1.00)      # normal dot border
fat_stroke_str =  str(lntk * 1.66)      # thicker border, used for root dots

# draw_dots tuples default formats
# --------------------------------
# Every dot drawn on the fretboard gets its look from a 13 elements tuple.
# Index and meaning of every element:
#
#    0  dot_radius_scale      Number, 1.0 = normal size, 0.9 = 10% smaller
#    1  dot_fill              String, color inside the dot ('black', '#ff0000', ...)
#    2  dot_fill_opacity      String, '0.0' (transparent) .. '1.0' (opaque)
#    3  dot_stroke            String, color of the dot border
#    4  dot_stroke_opacity    String, '0.0' .. '1.0'
#    5  dot_stroke_dasharray  String, 'none' for a solid border,
#                             'dashes' for an automatic dashed border
#    6  dot_stroke_width      String, border width
#    7  label_fill            String, color of the text inside the dot
#    8  label_fill_opacity    String, '0.0' .. '1.0'
#    9  dot_labelfont_weight  String, 'normal' or 'bold' ('' = global font weight)
#   10  dot_labelfont_family  String, font name ('' = global font family)
#   11  dot_isquare           Boolean, True draws a square instead of a circle
#   12  dot_rotate            Boolean, True rotates the dot shape by 90 degrees
#
# Formats are grouped in dicts {interval: tuple}. The key is an interval in
# lower case ('r' is the root, 'b3', '5', 'rh', ...) and '*' is the format used
# for every interval without a format of its own. There are two dicts:
#    fretb_format -> dots on the fretboard (fret >= 1)
#    fret0_format -> dots above the nut (fret 0, only drawn with --nut)
#
# if not set, dot_labelfont_weight and dot_labelfont_family default to
# global font weight and global font family

# black dot with white label: any note on the fretboard
tpl_generic_format = (1.0, 'black', '1.0', 
                      'black', '1.0', 'none', slim_stroke_str, 
                      'white', '1.0', '', '', 
                      False, False)
# white dot with dashed border: open string (fret 0) above the nut
tpl_fret0_format =   (1.0, 'white', '1.0', 
                      'black', '1.0', 'dashes',  slim_stroke_str, 
                      'black', '1.0', '', '', 
                      False, False)

# grey dot with thick border: root note on the fretboard (only with --root-diff)
tpl_generic_root_format = (1.0, 'lightgrey', '1.0', 
                           'black', '1.0', 'none', fat_stroke_str, 
                           'black', '1.0', '', '', 
                           False, False)
# grey dot with dashed border: open string root note (only with --root-diff)
tpl_fret0_root_format =   (1.0, 'lightgrey', '1.0', 
                           'black', '1.0', 'dashes', slim_stroke_str, 
                           'black', '1.0', '', '', 
                           False, False)


# default params dict
#--------------------
# Value used for every parameter that is set neither on the command line
# nor in the json config file. Keys are the same names used in the json
# config file (see tests/json_cfg_tests_files/default_chords_config.json)
default_params = {

    # --- core internal parameters

      'lntk': lntk                        # grid line tickness
    , 'barre_strk_wdth': barre_strk_wdth  # barre arc tickness
    , 'fd': fd                            # fret distance
    , 'sd': sd                            # string distance, optimal ratio is fd/sd = 1.3
                                          # image_w = (6.30*sd) + 43.0
                                          # image_h = (9.79*sd) + 43.0
    , 'ns': 6                             # number of strings, is 6 for guitar
    , 'nf': 4                             # number of frets, should be no more than 4 for chords
    , 'radius_factor': radius_factor      # sd factor to get global dot radius
    , 'x_or': 20.0                        # fretboard box origin offset (x)
    , 'y_or': 20.0                        # fretboard box origin offset (y)
    , 'debug': False                      # if true draw debug borders and debug dots
    # --- html report parameters
    , 'ncols': 4                          # number of columns for the gallery
    , 'thumb_width': '250.0px'            # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    
    # default params that can be set by cli and/or config_file
    
    , 'dir_output': './'                    # output dir for images
    , 'horiz': False                        # if true chord is horizontal otherwise vertical
    , 'chord_label_isbottom': False         # if true chord main label goes at the bottom
    , 'chord_label_isleft': False           # if true chord main label is left aligned otherwise is centered
    , 'enable_header': True                 # draw labels above fret zero
    , 'enable_dotlabels': True              # draw dot labels
    , 'enable_footer': False                # draw footer labels
    , 'enable_barre': True                  # draw barre
    , 'enable_fretnum': True                # draw reference fret number
    , 'nutline': True                       # draw nut line ticker
    , 'fret0': False                        # draw virtual dots above nut
    , 'root_is_different': False            # draw different dots for root note
    , 'font_family': 'Ubuntu Mono Legacy'   # global font family
    , 'font_weight': 'normal'               # global font weight
    , 'convert_flag': False                 # convert images to png files 
    , 'report': 'disable'                   # generate html report

    # default params that can be set by config_file only
    
    , 'chord_label_font_family': None           # main chord label font family: default is global font family
    , 'chord_label_font_weight': None           # main chord label font weight: default is global font weight
    , 'chord_label_font_factor': None           # main chord label font size factor: default is 0.70
    , 'upper_labels_font_family': None          # upper labels font family: default is global font family
    , 'upper_labels_font_weight': None          # upper labels font weight: default is global font weight
    , 'upper_labels_font_factor': None          # upper labels font factor: default is 1.15
    , 'bottom_labels_font_family': None         # bottom labels font family: default is global font family
    , 'bottom_labels_font_weight': None         # bottom labels font weight: default is global font weight
    , 'bottom_labels_font_factor': None         # bottom labels font factor: default is 1.00
    , 'side_labels_font_family': None           # side labels font family: default is global font family
    , 'side_labels_font_weight': None           # side labels font weight: default is global font weight
    , 'side_labels_font_factor': None           # side labels font factor: default is 0.90
    # draw_dots tuples formats: see the 13 elements tuple description above
    # fretboard format (by default every dot, root included, looks the same)
    , 'fretb_format': {
          '*': tpl_generic_format
        , 'r': tpl_generic_format
        }
    # fret0 format (dots above the nut)
    , 'fret0_format': {
          '*': tpl_fret0_format
        , 'r': tpl_fret0_format
        }

}



# =============================================================================
# main program
# =============================================================================
# this code runs only when the file is executed as a program
# (python3 fancychords.py ...), not when it is imported by another module
if __name__ == "__main__":

    program_version = '0.7'
    program_author = 'Simone Felli'
    
    # parser declaration
    # all the optional arguments that are to be checked by check() function
    # must default to None for script to work, see param_check() function
    
    parser = argparse.ArgumentParser(
          description='Simple chords drawing program'
        , prog='fancychords'        
        , epilog='Have fun playing guitar!'
        )

    # --- required arguments ---

    # create a mutually exclusive group, one for single chord input by cli through a string
    # one for single/multiple chord input by file with. Note one option is required
    excl_group = parser.add_mutually_exclusive_group(required=True)
    
    # chords_str is a sequence of onechord_str strings  divided by ';'
    # onechord_str is an input candidate single chord string:
    #    'chord_name|frets|fingers|intervals|dlabels|footer|subfolder', 
    #    separator is '|', only chord_name, frets are mandatory, if a non mandatory 
    #    parameters is to be given but some preceding ones are to be skipped use '%'
    excl_group.add_argument(
        '--cli_in'
        , action='store'
        , dest='chords_str'
        , help='input chord/s by cli string'
        )
    # input chord/s file path
    excl_group.add_argument(
        '--file_in'
        , action='store'
        , dest='input_crdf'
        , help='input chord/s by text file'
        )

    # --- optional arguments ---
    # note on boolean flags: they all use default=None (not False/True).
    # None means "not given on the command line", so param_check() can
    # fall back to the json config file value and then to default_params.
    # 'store_true' flags turn something on, 'store_false' flags (the --no-xxx
    # ones) turn off something that is on by default

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
        , help='draw chords horizontally, default is ' 
            + str(default_params['horiz'])
        )
    parser.add_argument(
        '-lb', '--label_bottom'
        , action="store_true"
        , dest='chord_label_isbottom'
        , default=None
        , help='main label goes at the bottom, default is ' 
            + str(default_params['chord_label_isbottom'])
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
        '-nb', '--no-barre'
        , action="store_false"
        , dest='enable_barre'
        , default=None
        , help='do not draw barre, barre is enabled by default'
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
        , choices=['Ubuntu Mono Legacy', 'Ubuntu Mono', 'Liberation Mono', 'DejaVu Sans Mono', 'Courier New']
        , help='global font family: [\'Ubuntu Mono Legacy\'|\'Ubuntu Mono\'|\'Liberation Mono\'' \
               '|\'DejaVu Sans Mono\'|\'Courier New\'], default is \'' 
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
               'report but do not draw chords, default is \'' 
                + str(default_params['report']) + '\''
        )


    # -- main call of the parser --

    # everything below is inside a try block: any error ends the program
    # with a clean message (see the 'except' at the end of the file)
    try:

        # read the command line. argparse itself handles --help, --version
        # and wrong options (printing usage and exiting with status 2)
        args = parser.parse_args()
        
        '''
        # for testing fancychords
        args = parser.parse_args(
            [  
            #  '--file_in', './tests/crds_test_files/chord-list.txt'
               '--cli_in', 'Gm(add11)|x,0,0,2,1,0|x,x,x,3,1,x|x,R,11,R,b3,5|%|x,x,x,3,1,x|G/Minor'
             , '-o', './dirout/'
             , '-r', 'enable'
             , '-rd'
             , '-c'
             , '-cf', './tests/json_cfg_tests_files/config.json'
             ]
            )
        '''

        if args:

            # content of the json config file ({} if no config file is given)
            db_dict_jdump = {}
            # 'file' or 'string', tells chords2files how to read input_crds
            input_way = ''
            
            # take note (using variable input_way)
            # if cli or input file was used to input chord/s
            if args.input_crdf:
                # input file was used to input chord/s
                input_crds = args.input_crdf
                input_way = 'file'
            else:
                # cli was used to input chord/s
                input_crds = args.chords_str
                input_way = 'string'
            
            # if a json config file was passed as argument
            if args.json_file:
                # load its content in db_dict_jdump. The json file has sections
                # ('i/o', 'flags', 'generic_formats', 'parameters') and every
                # section is a dict of parameters, ie:
                # {"flags": {"horiz": false, ...}, "parameters": {"sd": 50.0, ...}}
                import json
                json_file = args.json_file
                with open(json_file, 'r', encoding='utf-8') as jsonfile:
                    db_dict_jdump = json.load(jsonfile)
                    # add missing parameters if any (see fill_jdump function: take the json config file 
                    # db_dict_jdump and check if there are missing parameters that can be calculated 
                    # from others with known formulas, if so db_dict_jdump is modified in place with 
                    # missing parameters added)
                    global_utilities.fill_jdump(db_dict_jdump, FD_FACTOR, RADIUS_FACTOR_K, BARRE_FACTOR)
        
        # Get all the variables using param_check() function
        # as this function applies precedence logic: check if a parameter of fancychords is set 
        # by cli, by config file or is just as default. This logic applies: cli has highest precedence, 
        # then comes json config file and at last default. Return a Tuple:
        # - param value (type varies) set by precedence logic
        # - boolean, param is as default or not
        
        # note: param_check(db_dict_jdump, cli_value, name, json_section, defaults)
        # returns (value, is_default). [0] keeps only the value

        # params that can be set by cli and/or config_file
        dir_output = global_utilities.param_check(
            db_dict_jdump, args.dir_output, 
            'dir_output', 'i/o', 
            default_params)[0]
        horiz = global_utilities.param_check(
            db_dict_jdump, args.horiz, 
            'horiz', 'flags', 
            default_params)[0]
        chord_label_isbottom = global_utilities.param_check(
            db_dict_jdump, args.chord_label_isbottom, 
            'chord_label_isbottom', 'flags', 
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
        enable_barre = global_utilities.param_check(
            db_dict_jdump, args.enable_barre, 
            'enable_barre', 'flags', 
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
        # (None is passed as cli value, as there is no cli option for them)
        chord_label_font_weight = global_utilities.param_check(
            db_dict_jdump, None, 
            'chord_label_font_weight', 'generic_formats', 
            default_params)[0]
        chord_label_font_family = global_utilities.param_check(
            db_dict_jdump, None, 
            'chord_label_font_family', 'generic_formats', 
            default_params)[0]
        chord_label_font_factor = global_utilities.param_check(
            db_dict_jdump, None, 
            'chord_label_font_factor', 'generic_formats', 
            default_params)[0]
        chord_label_isleft = global_utilities.param_check(
            db_dict_jdump, None, 
            'chord_label_isleft', 'flags', 
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
        # for the two dot formats we also keep the "is default" flag: it is
        # needed below to decide if --root-diff can change them
        fretb_format, fretb_asdefault = global_utilities.param_check(
            db_dict_jdump, None, 
            'fretb_format', 'generic_formats', 
            default_params)
        fret0_format, fret0_asdefault = global_utilities.param_check(
            db_dict_jdump, None, 
            'fret0_format', 'generic_formats', 
            default_params)
        barre_strk_wdth = global_utilities.param_check(
            db_dict_jdump, None, 
            'barre_strk_wdth', 'parameters', 
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
        
        # app_msg_str collects every message of the run (it is also printed
        # step by step by the called functions)
        app_msg_str = '\nGlobal Options\n=============='
        
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.
        app_msg_str += ('{:<22} {} {:<22} {} {:<22} {} {:<22} {} {:<22} {}').format(
            '\ninput chord/s mode:', input_way,
            '\nconfig file:', str(args.json_file),            
            '\nroot is different:', root_is_different,
            '\nreport:', report,
            '\nconvert flag:', convert_flag
            )
        
        print(app_msg_str)
        
        
        # main functions call
        # report can be:
        #   'disable' -> draw chords, no html report (default)
        #   'enable'  -> draw chords, then build the html report
        #   'only'    -> do not draw anything, just (re)build the html report
        #                from the images already in dir_output
        
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
            
            
            # import function to draw/output chords
            # (imported here: it needs svgwrite and cairosvg)
            from libs import chords2files
            
            (  process_chords_msg_str
             , svg_file_path_list
             , png_file_path_list) = chords2files.process_chords(
                input_crds, input_way, 
                dir_output, horiz, enable_header, enable_dotlabels, 
                enable_footer, enable_barre, enable_fretnum,
                barre_strk_wdth, nutline, fret0,
                font_weight, font_family,
                chord_label_font_weight, chord_label_font_family, 
                chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
                fretb_format, fret0_format,
                upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
                bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
                side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
                lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, 
                convert_flag, debug
                )

            app_msg_str += '\n' + process_chords_msg_str

        if report != 'disable':

            # local libraries imports
            from libs import htmlreport 

            # the report shows every image with these extensions found in
            # dir_output and in its subdirs (one fcreport.html for every dir)
            file_exts = (".svg", ".png")
            app_msg_str += htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)


    # any error (ie a missing input file or a broken json config file) ends
    # the program with a short message on stderr and exit status 1, so that
    # scripts calling fancychords can tell a failed run from a good one
    # (before, the error was printed on stdout and the exit status was 0)
    except Exception as e:
        print('fancychords error: ' + str(e), file=sys.stderr)
        sys.exit(1)
