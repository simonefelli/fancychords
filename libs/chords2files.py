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
chords2files: main engine of fancychords, from input chords to image files.

process_chords() is called by fancychords.py and runs the whole job:

    1. prints an options summary (nice_print_options)
    2. reads the chords, from a cli string or from a text file, using
       chord_parser (validation, duplicate filenames fix)
    3. chord_list_to_files():
       - for every chord creates its output dir (dir_output + subfolder)
         and calls draw_chords.chord_to_file() to write the svg file
       - if convert_flag is True converts the svg files just drawn to png,
         in a 'png' subdir next to them (convert_svg2png)

Every function returns a message string with what was done, so that the
caller can collect a log of the whole run.
"""


# standard library imports
import os

# local application imports
from libs import chord_parser
from libs import draw_chords
from libs import convert_svg2png


def nice_print_options(tabslen, fretb_format, fret0_format, **kwargs):
    '''
    Pretty print options for process_chords() function
    
    tabslen: Integer, number of spaces as tabulature
    fretx_format: Dict for draw_dots tuples formats (see docs)
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
    # kwargs = {'input_way': 'file', 'input_crds': '../tests/crds_test_files/ ...', ...}
    # myitem = ('input_way', 'file') ...
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
    return msg_str


def chord_list_to_files(
        crd_list, 
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
        ):
    """
    Draw svg/png chords from crd_list outputs in dir_output

    crd_list: List of lists, ie = [
            [     chord_name
                , root_note
                , chord_filename
                , frets
                , fingers
                , intervals
                , dlabels
                , footer
                , subfolder
                , chord_quality
                , chord_detail
                , chord_slash
            ], ...
        ]
        
    ie:
    
        [
            [
                  'SI11'
                , 'SI'
                , 'SI11'
                , ['x', '0', '9', '8', '0', '0']
                , ['x', 'x', '2', '1', 'x', 'x']
                , ['x', '7', 'R', '3', 'R', '11']
                , ['x', '7', 'R', '3', 'R', '11']
                , ['x', 'x', '2', '1', 'x', 'x']
                , 'out/dirout/'
                , '11'
                , '(no5)'
                , 'F#'
            ]
            , ..
        ]
        
        list element should not be null 
    dir_output: String, output dir for chord image
    horiz: Boolean, if true chord is horizontal otherwise vertical
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels
    barre_strk_wdth: Number, barre arc tickness
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    font_weight: String, font weight
    font_family: String, font family
    chord_label_font_weight: String, Main chord label, font weight
    chord_label_font_family: String, Main chord label, font family
    chord_label_font_factor: Number, Main chord label, font size factor
    chord_label_isbottom: Boolean, if true chord main label goes at the bottom
    chord_label_isleft: Boolean, if true chord main label is left aligned otherwise is centered
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
    upper_labels_font_weight: String, upper labels, font weight
    upper_labels_font_family: String, upper labels, font family 
    upper_labels_font_factor: Number, upper labels, font factor 
    bottom_labels_font_weight: String, bottom labels, font weight
    bottom_labels_font_family: String, bottom labels, font family   
    bottom_labels_font_factor: Number, bottom labels, font factor      
    side_labels_font_weight: String, side labels, font weight
    side_labels_font_family: String, side labels, font family 
    side_labels_font_factor: Number, side labels, font factor        
    x_or: fretboard box origin offset (x)
    y_or: fretboard box origin offset (y)
    lntk: grid line tickness
    ns: number of strings, is 6 for guitar
    nf: number of frets, should be no more than 4 for chords
    fd: fret distance
    sd: string distance, optimal ratio is fd/sd = 1.3
    radius_factor: Number, sd factor to get global dot radius, optimal value 0.38 or 0.41
    convert_flag: Boolean, if true output also png file
    debug: Boolean, if true draw debug borders and debug dots

    return Tuple: useful msg_str, svg_file_path_list, png_file_path_list
    """
    
    header = "\nDrawing SVG Chords\n=================="
    print(header)
    svg_msg_str = header
    # chords drawn in every output dir, used for png conversion:
    # {'./dirout/C/Major/': ['C', 'C.v02'], './dirout/': ['G'], ...}
    chord_filenames_by_dir = {}
    svg_file_path_list = []
    png_file_path_list = []
    for crd in crd_list:
        # unpack chord list by index (see chord_parser module docs)
        chord_name = crd[0]
        chord_filename = crd[2]
        frets = crd[3]
        fingers = crd[4]
        intervals = crd[5]
        dlabels = crd[6]
        footer = crd[7]
        subfolder = crd[8]
        # check if subfolder exist
        if subfolder:
            path_output = os.path.join(dir_output, subfolder)
        else:
            path_output = dir_output + '/'
        # if path_output does not exist then create it
        # (makedirs also creates every missing parent dir)
        if not os.path.isdir(path_output): os.makedirs(path_output)
        print_label1 = "* " + chord_filename
        print_label2 = " --> "
        svg_file_path = os.path.normpath(path_output + chord_filename + ".svg")
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.
        body = '{:<20} {:6} {}'.format(print_label1, print_label2, svg_file_path)
        print(body)
        svg_msg_str += '\n' + body
        draw_chords.chord_to_file(
            chord_name, chord_filename, frets, fingers, intervals, dlabels, footer,
            path_output, horiz, enable_header, enable_dotlabels,
            enable_footer, enable_barre, enable_fretnum,
            barre_strk_wdth, nutline, fret0,
            font_weight, font_family,
            chord_label_font_weight, chord_label_font_family, 
            chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
            fretb_format, fret0_format,
            upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
            bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
            side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
            lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, debug
            )
        # remember what was written, for the return value and png conversion
        svg_file_path_list.append(svg_file_path)
        chord_filenames_by_dir.setdefault(path_output, []).append(chord_filename)

    svg_info_str = '>>> ' + str(len(svg_file_path_list))  + ' svg files processed <<<'
    print(svg_info_str)
    svg_msg_str += '\n' + svg_info_str
    msg_str = svg_msg_str
    
    # converting to png part
    if convert_flag:
        # convert only the svg files drawn in this run, each one into a 'png'
        # subdir of its own dir. Note: other svg files that may already be in
        # dir_output (ie from a previous run) are left untouched
        # convert_list = [('./dirout/Seventh/', './dirout/Seventh/png/', ['C7', ...]), ...]
        convert_list = [
            (curr_dir_out, os.path.join(curr_dir_out, 'png/'), filenames)
            for curr_dir_out, filenames in chord_filenames_by_dir.items()
            ]
        convert_msg_str = ''
        header = "\nConverting SVG Chords to PNG\n============================"
        print(header)
        convert_msg_str += header
        for curr_dir_out, curr_png_path, filenames in convert_list:
            cmsg_str, png_fp_list = convert_svg2png.convert_svg2png(
                curr_dir_out, curr_png_path, filenames
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


def process_chords(
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
       ):
    """
    Draw chords (output svg/png) defined in either a chords string or a chords file
    and save them in a dir_output

    input_crds: String, can be a 
        - chord list file path, is a text file with evry line as (header line is skipped)
            NAME              FRETS         FINGERS       INTERVALS           DOT LABELS          FOOTER        SUBFOLDER
            G#dim7(no5)/F#    2,2,0,1,0,1   3,4,x,1,x,2   b7,b3,b5,R,b3,bb7   b7,b3,b5,R,b3,bb7   3,4,x,1,x,2   Diminished        
            only chord_name, frets are mandatory, if a non mandatory parameters 
            is to be given but some preceding ones are to be skipped use '%'
        - candidate chords string
            is a sequence of onechord_str strings divided by ';'. onechord_str is 
            an input candidate single chord string like this:
                'chord_name|frets|fingers|intervals|dlabels|footer|subfolder'
                separator is '|'
                only chord_name, frets are mandatory, if a non mandatory parameters 
                is to be given but some preceding ones are to be skipped use '%'
    input_way: String, what input_crds represent, can be either 'string' or 'file'
    dir_output: String, output dir for chord image
    horiz: Boolean, if true chord is horizontal otherwise vertical
    enable_header: Boolean, if True enable header labels
    enable_dotlabels: Boolean, if True enable dot labels
    enable_footer: Boolean, if True enable footer labels
    enable_barre: Boolean, if true draw barre/s on chord
    enable_fretnum: Boolean, if true enable side labels
    barre_strk_wdth: Number, barre arc tickness
    nutline: Boolean, if True draw nut line ticker
    fret0: Boolean, if True you can draw dots above nut
    font_weight: String, font weight
    font_family: String, font family
    chord_label_font_weight: String, Main chord label, font weight
    chord_label_font_family: String, Main chord label, font family
    chord_label_font_factor: Number, Main chord label, font size factor
    chord_label_isbottom: Boolean, if true chord main label goes at the bottom
    chord_label_isleft: Boolean, if true chord main label is left aligned otherwise is centered
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
    upper_labels_font_weight: String, upper labels, font weight
    upper_labels_font_family: String, upper labels, font family 
    upper_labels_font_factor: Number, upper labels, font factor 
    bottom_labels_font_weight: String, bottom labels, font weight
    bottom_labels_font_family: String, bottom labels, font family   
    bottom_labels_font_factor: Number, bottom labels, font factor      
    side_labels_font_weight: String, side labels, font weight
    side_labels_font_family: String, side labels, font family 
    side_labels_font_factor: Number, side labels, font factor       
    root_is_square: Boolean, if true draw square dots for root note 
    x_or: Number, fretboard box origin (x)
    y_or: Number, fretboard box origin(y)  
    lntk: Number, grid line tickness    
    ns: Number, number of strings, is 6 for guitar
    nf: Number, number of frets, should be no more than 4 for chords
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
    # (used only for printing: None means "use the global value")
    shortenop = lambda x: x if x is not None else 'default'

    # outputs a useful option summary for information
    option_summary = '\nChords Options Summary\n======================'
    option_summary += nice_print_options(
         37
        , fretb_format
        , fret0_format
        , input_way=input_way
        , input_crds=input_crds[0:25]+' ...' if len(input_crds) > 26 else input_crds
        , dir_output=dir_output
        , horiz=horiz
        , enable_header=enable_header
        , enable_dotlabels=enable_dotlabels
        , enable_footer=enable_footer
        , lntk=lntk
        , enable_barre=enable_barre
        , barre_strk_wdth=barre_strk_wdth
        , nutline=nutline
        , fret0=fret0
        , font_weight=font_weight
        , font_family=font_family
        , convert_flag=convert_flag
        , chord_label_font_weight=shortenop(chord_label_font_weight)
        , chord_label_font_family=shortenop(chord_label_font_family)
        , chord_label_font_factor=shortenop(chord_label_font_factor)
        , chord_label_isbottom=shortenop(chord_label_isbottom)
        , chord_label_isleft=shortenop(chord_label_isleft)
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

    # os normalize dir: './out//a/../b/' -> 'out/b'
    # (also turns '/' into '\\' on Windows)
    dir_output = os.path.normpath(dir_output)
    
    if input_way == 'string':
        
        # ';' splitting: one string for every chord
        # 'C|x,3,2,0,1,0;G|3,2,0,0,0,3' -> ['C|x,3,2,0,1,0', 'G|3,2,0,0,0,3']
        chords_str_split = input_crds.split(';')
        
        # '|' splitting: one list of fields for every chord
        # ['C|x,3,2,0,1,0', ...] -> [['C', 'x,3,2,0,1,0'], ...]
        # - blank chunks (ie a trailing ';' or '; ') are skipped, otherwise they
        #   would be parsed as a chord without a name
        # - an empty field between two '|' (ie 'C|x,3,2,0,1,0||x,R,3,5,R,3')
        #   means "skip this field", exactly like '%'. It must be turned into
        #   '%' here because chord_parser drops empty fields (needed for text
        #   files, where many tabs are used just to align columns) and every
        #   following field would shift one column to the left
        chords_str_list = [
            [field if field.strip() else '%' for field in onechord_str.strip().split('|')]
            for onechord_str in chords_str_split if onechord_str.strip()
            ]

        # crd_list = [[chord_name, chord_filename, frets, fingers, dlabels, footer, subfolder], ...]
        # crd_list_msg_str -> (crd_list, msg_str)
        (crd_list, crd_list_msg_str) = chord_parser.get_crd_list_from_str_list(chords_str_list)    

    elif input_way == 'file':

        # os normalize dirs and files paths
        input_crdf = os.path.normpath(input_crds)
        
        # crd_list = 
        #  [  
        #      [
        #         chord_name
        #       , root_note
        #       , chord_filename
        #       , frets
        #       , fingers
        #       , intervals
        #       , dlabels
        #       , footer
        #       , subfolder
        #       , chord_quality
        #       , chord_detail
        #       , chord_slash
        #     ], ...
        #  ]
        
        # get_crd_list_from_file -> (crd_list, msg_str)
        (crd_list, crd_list_msg_str) = chord_parser.get_crd_list_from_file(input_crdf)    

    # print some info
    info_msg_str = '\nChords to draw (' + str(len(crd_list)) + \
          ' chords):\n==============================='
    for elem in crd_list:
        chord_name = elem[0]
        # root_note = elem[1]
        frets = elem[3]
        fingers = elem[4]
        interv = elem[5]
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.
        info_msg_str += '\n{:<20} {:20}  {:20}  {:20}'.format(
                  '* ' + chord_name
                , ','.join(frets)
                , ','.join(fingers)
                , ','.join(interv)
                )
    print(info_msg_str)

    # main draw svg part
    (  chord_list_to_files_msg_str
    , svg_file_path_list
    , png_file_path_list) = chord_list_to_files(
        crd_list, dir_output, horiz,
        enable_header, enable_dotlabels, enable_footer,
        enable_barre, enable_fretnum,
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

    crd_list_msg_str += '\n' + info_msg_str + '\n' + chord_list_to_files_msg_str
    
    return option_summary + '\n' + crd_list_msg_str, svg_file_path_list, png_file_path_list


if __name__ == "__main__":
    
    # local application imports
    from libs import htmlreport

    # --- internal parameters ---
    sd = 50.00                      # string distance, optimal ratio is fd/sd = 1.30
                                    # image_w = (6.30*sd) + 43.0
                                    # image_h = (9.79*sd) + 43.0
    lntk = 3.00                     # grid line tickness
    x_or = 20.00                    # fretboard box origin offset (x)
    y_or = 20.00                    # fretboard box origin offset (y)
    ns = 6                          # number of strings, is 6 for guitar
    nf = 4                          # number of frets, should be no more than 4 for chords
    debug = False                   # if true draw debug borders and debug dots
    #  --- derived internal parameters ---
    fd = sd * 1.30                  # fret distance                                
    radius_factor = 20.00 / sd      # sd factor to get global dot radius, optimal value 0.38 or 0.41
                                    # as a guideline: radius_factor = (20.00/sd)
                                    # general formula for radius is: radius = sd * radius_factor
                                    # single dot adjustments can be achieved through dot_radius_scale
                                    # in fretx_format tuples                                 
    barre_strk_wdth = 1.10 * lntk   # barre arc tickness
    
    # --- html report parameters
    report = 'enable'       # generate html report [ 'only' | 'enable' | 'disable' ]    
    ncols = 4               # number of columns for the gallery
    thumb_width = '300.0px' # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)

    # --- main parameters
    dir_output = '../dirout'                # output dir for images
    horiz = False                           # if true chord is horizontal otherwise vertical
    chord_label_isbottom = False            # if true chord main label goes at the bottom
    chord_label_isleft = False              # if true chord main label is left aligned otherwise is centered
    enable_header = True                    # if True enable header labels
    enable_dotlabels = True                 # if True enable dot labels
    enable_footer = True                    # if True enable footer labels
    enable_barre = True                     # if true draw barre/s on chord
    enable_fretnum = True                   # if true enable side labels
    nutline = True                          # if True draw nut line ticker
    fret0 = True                            # if True you can draw dots above nut
    convert_flag = True                     # if true output also png file
    font_weight = 'normal'                  # global font weight: [ 'normal' | 'bold' ]
    font_family = 'Ubuntu Mono derivative FChords'             # global font family: ['Courier New' | 'Ubuntu Mono' | 
                                            # 'DejaVu Sans Mono' | 'Liberation Mono']

    # --- appearance  parameters
    chord_label_font_weight = None          # main chord label, font weight
    chord_label_font_family = None          # main chord label, font family 
    chord_label_font_factor = None          # main chord label, font size factor: default is 0.70
    upper_labels_font_weight = None         # upper labels, font weight
    upper_labels_font_family = None         # upper labels, font family   
    upper_labels_font_factor = None         # upper labels, font size factor: default is 1.15
    bottom_labels_font_weight = None        # bottom labels, font weight
    bottom_labels_font_family = None        # bottom labels, font family      
    bottom_labels_font_factor = None        # bottom labels, font size factor: default is 1.00
    side_labels_font_weight = None          # side labels, font weight
    side_labels_font_family = None          # side labels, font family
    side_labels_font_factor = None          # side labels, font size factor  : default is 0.90
                           
    # calculate fretx_format dot_stroke_width from lntk
    slim_stroke_str = str(lntk * 1.00)
    fat_stroke_str =  str(lntk * 1.66)

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
                'white', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'none', fat_stroke_str,
                 'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                 False, False)
    }
    
    fret0_format = {
          '*': (1.0, 'white', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
        , 'r': (1.0, 'lightgrey', '1.0', 
                'black', '1.0', 'dashes', slim_stroke_str, 
                'black', '1.0', 'normal', 'Ubuntu Mono derivative FChords', 
                False, False)
    }



    # testing process_chords
    

    
    input_crds = '../tests/crds_test_files/chords2files_chord-list.txt'        # full path for chord list txt
    
    input_way = 'file'

    '''
    
    input_crds = 'Bsus(maj)|x,0,0,2,1,0|%|%|%|%|B/Sus;Bsus(maj)|x,1,3,3,2,1|%|%|%|%|B/Sus'
    
    input_way = 'string'
    
    '''
    
    # check if report has to be done
    if report != 'only':
        (  process_chords_msg_str
         , svg_file_path_list
         , png_file_path_list) = process_chords(
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
            convert_flag, debug)
    if report != 'disable':
        file_exts = ('.svg', '.png')
        process_chords_msg_str += '\n' + htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)
    
    print(process_chords_msg_str)
    # print(svg_file_path_list)
    # print(png_file_path_list)
