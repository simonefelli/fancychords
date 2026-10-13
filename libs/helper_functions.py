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
from libs import music_utilities
from libs import global_constants
from libs import global_utilities
from libs import chord_parser
from libs import scale_parser
from libs import chords2files
from libs import scales2files
from libs import htmlreport


def trunk_scales(in_frets, in_intervals, in_dlabels, lower_fret, higher_fret):
    '''
    take a scale (defined as frets, intervals and dlabels string lists) and 
    trunk it left and right down to lower_fret and up to
    higher_fret. If lower_fret, higher_fret are inconsistent then 
    output original input lists (do nothing), ie:
    
    in_frets = [
          ['x', '5', 'x', 'x', '8', 'x']
        , ['x', '5', 'x', 'x', '8', 'x']
        , ['x', '5', 'x', '7', '8', 'x']
        , ['x', '5', 'x', '7', 'x', 'x']
        , ['x', '5', '6', '7', 'x', 'x']
        , ['x', '5', 'x', 'x', '8', 'x']
        ]
    --> f(.. lower_fret=5, higher_fret=7) -->
    out_frets = [
          ['5', 'x', 'x']
        , ['5', 'x', 'x']
        , ['5', 'x', '7']
        , ['5', 'x', '7']
        , ['5', '6', '7']
        , ['5', 'x', 'x']
        ]
        
    in_frets: list of string lists (6 elements, one for every guitar String - frets positions)
        ie: [['5', '5', '5', '5', '5', '5'], ['x', '6', 'x', 'x', 'x', 'x'], ...]
    in_intervals: list of string lists (6 elements, one for every guitar String - intervals positions), optional
        ie: [['R', '4', 'b7', 'b3', '5', 'R'], ['x', 'b5', 'x', 'x', 'x', 'x'], ...]
    in_dlabels: list of string lists (6 elements, one for every guitar String - dlabels positions), optional
        ie: [['1', '1', '1', '1', '1', '1'], ['x', '2', 'x', 'x', 'x', 'x'], ...]
    lower_fret: Number, up fret limit for trunking
    higher_fret: Number, down fret limit for trunking
    
    return Tuple of 3 list:
        out_frets, out_intervals, out_dlabels
    '''
    # initialize output lists
    out_frets, out_intervals, out_dlabels = [], [], []
    if lower_fret is not None and higher_fret is not None:        # check for types
        if (type(lower_fret) == int) and (type(higher_fret) == int):
            # get max and min frets
            max_fret, min_fret = global_utilities.max_min_scales_slst(in_frets)
            # trunk only if these requirements are met
            if (min_fret<=lower_fret) and (max_fret>=higher_fret) and (higher_fret>=lower_fret):
                # trunk frets
                for strng in in_frets:
                    out_frets.append(
                        strng[lower_fret-min_fret:higher_fret-min_fret+1]
                        )
                # if intervals exist trunk them
                if in_intervals:
                    for intrv in in_intervals:
                        out_intervals.append(
                            intrv[lower_fret-min_fret:higher_fret-min_fret+1]
                            )
                # if dlabels exist trunk them
                if in_dlabels:
                    for dlbl in in_dlabels:
                        out_dlabels.append(
                            dlbl[lower_fret-min_fret:higher_fret-min_fret+1]
                            )
    if out_frets:
        return out_frets, out_intervals, out_dlabels
    else:
        return in_frets, in_intervals, in_dlabels


def pad_scales(in_frets, in_intervals, in_dlabels, lower_fret, higher_fret):
    '''
    take a scale (defined as frets, intervals and dlabels string lists) and 
    pad it with 'x' both left and right down to lower_fret and up to
    higher_fret. If lower_fret, higher_fret are inconsistent then 
    output original input lists (do nothing), ie:
    
    in_frets = [
          ['5', 'x', 'x', '8']
        , ['5', 'x', 'x', '8']
        , ['5', 'x', '7', '8']
        , ['5', 'x', '7', 'x']
        , ['5', '6', '7', 'x']
        , ['5', 'x', 'x', '8']
        ]
    --> f(.. lower_fret=4, higher_fret=9) -->
    out_frets = [
          ['x', '5', 'x', 'x', '8', 'x']
        , ['x', '5', 'x', 'x', '8', 'x']
        , ['x', '5', 'x', '7', '8', 'x']
        , ['x', '5', 'x', '7', 'x', 'x']
        , ['x', '5', '6', '7', 'x', 'x']
        , ['x', '5', 'x', 'x', '8', 'x']
        ]
        
    in_frets: list of string lists (6 elements, one for every guitar String - frets positions)
        ie: [['5', '5', '5', '5', '5', '5'], ['x', '6', 'x', 'x', 'x', 'x'], ...]
    in_intervals: list of string lists (6 elements, one for every guitar String - intervals positions), optional
        ie: [['R', '4', 'b7', 'b3', '5', 'R'], ['x', 'b5', 'x', 'x', 'x', 'x'], ...]
    in_dlabels: list of string lists (6 elements, one for every guitar String - dlabels positions), optional
        ie: [['1', '1', '1', '1', '1', '1'], ['x', '2', 'x', 'x', 'x', 'x'], ...]
    lower_fret: Number, up fret limit for padding
    higher_fret: Number, down fret limit for padding
    
    return Tuple of 3 list:
        out_frets, out_intervals, out_dlabels
    '''
    # initialize output lists
    out_frets, out_intervals, out_dlabels = [], [], []
    if lower_fret is not None and higher_fret is not None:
        # check for types
        if (type(lower_fret) == int) and (type(higher_fret) == int):
            # get max and min frets
            max_fret, min_fret = global_utilities.max_min_scales_slst(in_frets)
            # pad only if these requirements are met
            if (lower_fret<=min_fret) and (higher_fret>=max_fret):
                # pad frets
                for strng in in_frets:
                    out_frets.append(
                        ['x']*(min_fret-lower_fret) + \
                        strng + \
                        ['x']*(higher_fret-max_fret)
                        )
                # if intervals exist pad them
                if in_intervals:
                    for intrv in in_intervals:
                        out_intervals.append(
                            ['x']*(min_fret-lower_fret) + \
                            intrv + \
                            ['x']*(higher_fret-max_fret)
                            )
                # if dlabels exist pad them
                if in_dlabels:
                    for dlbl in in_dlabels:
                        out_dlabels.append(
                            ['x']*(min_fret-lower_fret) + \
                            dlbl + \
                            ['x']*(higher_fret-max_fret)
                            )
    if out_frets:
        return out_frets, out_intervals, out_dlabels
    else:
        return in_frets, in_intervals, in_dlabels
    

def generate_scale(root_note, scale_type, up_to_fret, print_output=True):
    '''
    generate a list with all scale infos, given root note, scale formula and fret upper neck limit
    
    root_note: String, root note
    
    scale_type: String, scale label in key of global_constants.scales_library dict
    
    up_to_fret: Number, upper limt in fret for the neck
    
    print_output: Optional Boolean param, if False do not print anything
    
    return: List, ie
    [
        root_note -> 'G'
        scale_name -> 'Blues Scale'
        [neck_frets] ->    [[None,  1,   None,  3,  None ...], [None,  1,   2,    3,  None ...] ...]
        [neck_intervls] -> [[None, 'b7', None, 'R', None ...], [None, '4', 'b5', '5', None ...] ...]
        [neck_notes] ->    [[None, 'F',  None, 'G', None ...], [None, 'C', 'Db', 'D', None ...] ...]
    ]
    
    '''
    # guitar neck lists in sharp/flat mode for 3 octaves and right trimmed to up_to_fret
    # guitar_neck_sharp_notes = [['E', 'F', 'F#', 'G', 'G#' ...], ['B', 'C', 'C#', 'D', 'D#' ...], ...]
    guitar_neck_sharp_notes = []
    # guitar_neck_flat_notes = [[['E', 'F', 'Gb', 'G', 'Ab' ...], ['B', 'C', 'Db', 'D', 'Eb' ...], ...]
    guitar_neck_flat_notes = []    
    
    # guitar_string = ['E', 'A', 'D', 'G', 'B', 'E']
    for gstring in global_constants.guitar_strings:
        gstring_notes = music_utilities.n_octaves(gstring, 3, 'sharp')[:up_to_fret+1]
        guitar_neck_sharp_notes.insert(0, gstring_notes)
    
    for gstring in global_constants.guitar_strings:
        gstring_notes = music_utilities.n_octaves(gstring, 3, 'flat')[:up_to_fret+1]
        guitar_neck_flat_notes.insert(0, gstring_notes)
    
    guitar_neck_notes = {
        'flat':  guitar_neck_flat_notes,
        'sharp': guitar_neck_sharp_notes
        }
    
    # scale_type= 'minor_blues_scale' -> ('R','b3','4','b5','5','b7'), 'minor', 'Minor Blues Scale'
    intervals, majmin, scale_name = global_constants.scales_library[scale_type]
    flsh = music_utilities.music_circle_flsh(root_note, majmin)
    # neck notes in correct flat or sharp based on music circle
    # [['E', 'F', 'Gb', 'G', 'Ab' ...], ['B', 'C', 'Db', 'D', 'Eb' ...], ...]
    neck_notes = guitar_neck_notes[flsh]
    
    # scale_notes is a dict {note: interval, ..} 
    # ie:  {'G': 'R', 'Bb': 'b3', 'C': '4', 'Db': 'b5', 'D': '5', 'F': 'b7'}
    scale_notes = {}
    for interv in intervals:
        hstep = music_utilities.interval_to_hstep(interv)
        mynote = music_utilities.hstep_to_note(root_note, hstep, flsh)
        scale_notes[mynote] = interv
    
    # dict_keys(['G', 'Bb', 'C', 'Db', 'D', 'F'])
    note_filter = scale_notes.keys()
    
    # filter neck notes with note filter
    neck_notes_fltrd = [
            [
                note if note in note_filter else None for note in gstr_notes
            ] for gstr_notes in neck_notes
        ]
    
    # get neck intervals
    neck_intervls_fltrd = [
            [
                scale_notes[note] if note in note_filter else None for note in gstr_notes
            ] for gstr_notes in neck_notes
        ]
    
    # get neck frets
    neck_frets_fltrd = [
            [
                id_el if note in note_filter else None for id_el, note in enumerate(gstr_notes)
            ] for gstr_notes in neck_notes
        ]
    
    my_scale = [
          root_note
        , scale_name
        , neck_frets_fltrd
        , neck_intervls_fltrd
        , neck_notes_fltrd
        ]
    
    if print_output:
        msg = 'GENERATING SCALE\n----------------'
        msg += '\nroot_note: ' + root_note
        msg += '\nscale_name: ' + scale_name
        msg += '\nneck_frets_fltrd:'
        for elem in neck_frets_fltrd: msg += '\n\t' + str(elem)
        msg += '\nneck_intervls_fltrd:'
        for elem in neck_intervls_fltrd: msg += '\n\t' + str(elem)
        msg += '\nneck_notes_fltrd:'
        for elem in neck_notes_fltrd: msg += '\n\t' + str(elem)
        msg += '\n'
        print(msg)
     
    return my_scale


def generate_scale_file(my_scale, my_scale_file, display_notes, print_output=True):
    '''
    generate a scale text file compatible with 
    scales2files.process_scales_file() function
    
    my_scale: List, return value of generate_scale() function, ie:
              [root_note, scale_name, neck_frets_fltrd, neck_intervls_fltrd, neck_notes_fltrd]
    
    my_scale_file: String, scale file text path
    
    display_notes: Boolean, if True display notes instead of intervals (default)
    
    print_output: Optional Boolean param, if False do not print anything
    
    return nothing, just create text file
    ''' 
    # my_scale list from generate_scale() function
    (
        root_note, scale_name, neck_frets_fltrd,
        neck_intervls_fltrd, neck_notes_fltrd
    ) = my_scale
    
    name_row = 'NAME\t\t' + root_note + ' ' + scale_name
    folder_row = 'FOLDER\t\t./'
    filename_row = 'FILENAME\t\t'
    footer_row = 'FOOTER\t\tE, A, D, G, B, e'
    arrows_row = 'ARROWS\t\t'
    file_content = name_row + '\n' + folder_row + '\n' + filename_row
    
    # shoul always be 6
    n_gstrings = len(neck_frets_fltrd)
    
    for indx in range(0, n_gstrings):
        
        # [None, 1, None, 3, None]
        fret_row_lst = neck_frets_fltrd[indx]
        # replace in list Nones with 'x ' and turn elements into left padded strings (3 -> '3 ') 
        #  ['x ', '1 ', 'x ', '3 ', 'x ']
        fret_row_str_lst = [str(elem).ljust(2) if elem is not None else 'x ' for elem in fret_row_lst]
        # ' x , 1 , x , 3 , x '
        fret_row_str = ', '.join(fret_row_str_lst)
        
        # replace in list Nones with 'x ' and left pad strings ('R' -> 'R ',  'b7' stays same) 
        #  [None, 'b7', None, 'R', None]
        intervls_row_lst = neck_intervls_fltrd[indx]
        # ['x ', 'b7', 'x ', 'R ', 'x ']
        intervls_row_str_lst = [str(elem).ljust(2) if elem is not None else 'x ' for elem in intervls_row_lst]
        # ' x , b7, x , R , x '
        intervls_row_str = ', '.join(intervls_row_str_lst)
        
        # replace in list Nones with 'x ' and left pad strings ('F' -> 'F ') 
        # [None, 'F', None, 'G', None]
        notes_row_lst = neck_notes_fltrd[indx]
        # ['x ', 'F ', 'x ', 'G ', 'x ']
        notes_row_str_lst = [str(elem).ljust(2) if elem is not None else 'x ' for elem in notes_row_lst]
        # 'x , F , x , G , x '
        notes_row_str = ', '.join(notes_row_str_lst)
        
        if display_notes:
            # 'STRING06    x , 1 , x , 3 , x         x , b7, x , R , x         x , F , x , G , x '
            gstring_row = 'STRING0' + str(indx+1) + '\t' + fret_row_str + '\t\t' + intervls_row_str + '\t\t' + notes_row_str
        else:
            # 'STRING06    x , 1 , x , 3 , x         x , b7, x , R , x         x , b7, x , R , x '
            gstring_row = 'STRING0' + str(indx+1) + '\t' + fret_row_str + '\t\t' + intervls_row_str + '\t\t' + intervls_row_str
        
        file_content += '\n' + gstring_row

    file_content += '\n' + footer_row + '\n' + arrows_row
    
    if print_output:
        msg = 'WRITING SCALE FILE\n------------------\n'
        msg += 'scale_file: ' + my_scale_file + '\n'
        msg += 'File content:\n**********\n' + file_content + '\n**********'
        print(msg)

    os.makedirs(os.path.dirname(my_scale_file), exist_ok=True)
    with open(my_scale_file, 'w') as f1:
        f1.write(file_content)


def process_chords_by_config_json(json_file_path, crd_list, **overload_params):
    '''
    Given an input crd_list and a json config file this function draw chords list
    using json file for setting configuration options. These options can be overloaded
    by **overload_params keyword arguments, ie:
    
    process_chords_by_config_json(
          json_file_path , crd_list
        , dir_output = './dirout/chords'
        , report = 'enable'
        )
        
    json_file_path: String, json file path

    crd_list: List of lists
    
    [
        [chord_name, root_note, chord_filename, 
        frets, fingers, intervals, dlabels, footer, 
        subfolder, chord_quality, chord_detail, chord_slash]
        , ...
    ]
    
    ie:
    
    [
        ['G#dim7(no5)/F#', 'G#', ''G#dim7(no5)_F#', 
        ['2', '2', '0', '1', '0', '1'], ['3', '4', 'x', '1', 'x', '2'], ['b7', 'b3', 'b5', 'R', 'b3', 'bb7'], 
        ['b7', 'b3', 'b5', 'R', 'b3', 'bb7'], ['3', '4', 'x', '1', 'x', '2'],
        'Diminished/', 'dim7','(no5)', 'F#']
        , ...
    ]
    
    **overload_params: keyword arguments, sequence of params and their value 
    (similar to a dict) ie: dir_output = './dirout/chords', report = 'enable'
    
    return Tuple: explicative message, svg_file_path_list, png_file_path_list
    '''
    
    # get all json params. They can be overloaded by **overload_params keyword arguments
    # process_chords_params -> params for process_chords function
    # report_params -> params for generate_htmlreport function
    process_chords_params, report_params  = global_utilities.overload_config_json(
          json_file_path
        , 'chords'
        , **overload_params
        )
    
    # variables for generate_htmlreport functions
    (
          report
        , dir_output
        , ncols
        , thumb_width
    ) = report_params


    # ------ useful message (input scales details)  ------
    
    print('\ncrd_list_from_file (' + str(len(crd_list)) + \
          ' chords):\n===============================')
    for elem in crd_list:
        chord_name = elem[0]
        # root_note = elem[1]
        frets = elem[3]
        # fingers = elem[4]
        interv = elem[5]
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.    
        print('{:<15} {:<35} {}'.format(chord_name, str(frets), str(interv)))
        
    # ----------------------------------------------------

    # check if report has to be done and process chords
    if report != 'only':
        # main function call
        (
            chord_list_to_files_msg_str
          , svg_file_path_list
          , png_file_path_list
        ) = chords2files.chord_list_to_files(
            crd_list, 
            *process_chords_params
           )
    if report != 'disable':
        file_exts = ('.svg', '.png')
        htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)
    
    return chord_list_to_files_msg_str , svg_file_path_list, png_file_path_list


def process_chordsfile_by_config_json(json_file_path, input_crdf, **overload_params):
    '''
    Given an input chords file and a json config file this function draw chords list
    using json file for setting configuration options. These options can be overloaded
    by **overload_params keyword arguments, ie:
    
    process_chordsfile_by_config_json(
          json_file_path , input_crdf
        , dir_output = './dirout/chords'
        , report = 'enable'
        )
        
    json_file_path: String, json file path

    input_crdf: String, chords file path
    
    **overload_params: keyword arguments, sequence of params and their value 
    (similar to a dict) ie: dir_output = './dirout/chords', report = 'enable'
    
    return Tuple: explicative message, svg_file_path_list, png_file_path_list
    '''
    
    # get all json params. They can be overloaded by **overload_params keyword arguments
    # process_chords_params -> params for process_chords function
    # report_params -> params for generate_htmlreport function
    process_chords_params, report_params  = global_utilities.overload_config_json(
          json_file_path
        , 'chords'
        , **overload_params
        )
    
    # variables for generate_htmlreport functions
    (
          report
        , dir_output
        , ncols
        , thumb_width
    ) = report_params
    
    # ------ useful message (input scales details)  ------
    
    # get_crd_list_from_file -> (
    #   crd_list
    # , msg_str
    # )
    
    # crd_list = [
    #   [
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
    #   ], ..
    # ]

    return_crd_list_from_file = chord_parser.get_crd_list_from_file(input_crdf, print_output=False)[0]
    print('\ncrd_list_from_file (' + str(len(return_crd_list_from_file)) + \
          ' chords):\n===============================')
    for elem in return_crd_list_from_file:
        chord_name = elem[0]
        # root_note = elem[1]
        frets = elem[3]
        # fingers = elem[4]
        interv = elem[5]
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.   
        print('{:<15} {:<35} {}'.format(chord_name, str(frets), str(interv)))
        
    # ----------------------------------------------------

    # variable for chords2files.process_chords function
    input_way = 'file'

    # check if report has to be done and process chords
    if report != 'only':
        # main function call
        (
            chord_list_to_files_msg_str
          , svg_file_path_list
          , png_file_path_list
        ) = chords2files.process_chords(
            input_crdf, input_way,
            *process_chords_params
           )
    if report != 'disable':
        file_exts = ('.svg', '.png')
        htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)
    
    return chord_list_to_files_msg_str , svg_file_path_list, png_file_path_list


def process_scales_by_config_json(json_file_path, scl_list, **overload_params):
    '''
    Given an input scales list and a json config file this function draw scales list
    using json file for setting configuration options. These options can be overloaded
    by **overload_params keyword arguments, ie:
    
    process_scales_by_config_json(
          json_file_path , scl_list
        , dir_output = './dirout/scales'
        , report = 'enable'
        )
        
    json_file_path: String, json file path

    scl_list: list of list, each list is a scale:
    [
        [
           error_in_scale
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
    
    ie:
    
    [
        [
              False
            , ''
            , 'Am Blues Scale, Position 2'
            , 'Am_Blues_Scale2'      
            , './Blues_Scale'
            , [['5', 'x', 'x', '8'], ['5', 'x', 'x', '8'], ...]
            , [['R', 'x', 'x', 'b3'], ['5', 'x', 'x', 'b7'], ...]
            , [['1', 'x', 'x', '4'], ['1', 'x', 'x', '4'], ...]
            , ['E', 'A', 'D', 'G', 'B', 'e']
            , [((5, 2), (8, 2)), ((5, 4), (7, 4)), ((6, 5), (7, 5))]
        ], ..
    ]
    
    **overload_params: keyword arguments, sequence of params and their value 
    (similar to a dict) ie: dir_output = './dirout/scales', report = 'enable'
    
    return Tuple: explicative message, svg_file_path_list, png_file_path_list
    '''

    # get all json params. They can be overloaded by **overload_params keyword arguments
    # process_scales_params -> params for process_scales_file function
    # report_params -> params for generate_htmlreport function
    process_scales_params, report_params  = global_utilities.overload_config_json(
          json_file_path
        , 'scales'
        , **overload_params
        )
    
    # variables for generate_htmlreport functions
    (
          report
        , dir_output
        , ncols
        , thumb_width
    ) = report_params


    # ------ useful message (input scales details)  ------

    print('\nscl_list (' + str(len(scl_list)) + \
          ' scales):\n===============================')
    for elem in scl_list:
        scale_name = elem[2]
        # root_note = elem[1]
        frets = elem[5]
        interv = elem[6]
        print(scale_name)
        print('* frets')
        for elem in frets: print('  ' + str(elem))
        print('* interv')
        for elem in interv: print('  ' + str(elem))
        
    # ----------------------------------------------------

    # check if report has to be done and process chords
    if report != 'only':
        # main function call
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list
         ) = scales2files.scale_list_to_files(
            scl_list, 
            *process_scales_params
           )
    if report != 'disable':
        file_exts = ('.svg', '.png')
        htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)
    
    return process_scales_msg_str, svg_file_path_list, png_file_path_list


def process_scalesfile_by_config_json(json_file_path, input_sclf, **overload_params):
    '''
    Given an input scales file and a json config file this function draw scales list
    using json file for setting configuration options. These options can be overloaded
    by **overload_params keyword arguments, ie:
    
    process_scalesfile_by_config_json(
          json_file_path , input_sclf
        , dir_output = './dirout/scales'
        , report = 'enable'
        )
        
    json_file_path: String, json file path

    input_sclf: String, scales file path
    
    **overload_params: keyword arguments, sequence of params and their value 
    (similar to a dict) ie: dir_output = './dirout/scales', report = 'enable'
    
    return Tuple: explicative message, svg_file_path_list, png_file_path_list
    '''

    # get all json params. They can be overloaded by **overload_params keyword arguments
    # process_scales_params -> params for process_scales_file function
    # report_params -> params for generate_htmlreport function
    process_scales_params, report_params  = global_utilities.overload_config_json(
          json_file_path
        , 'scales'
        , **overload_params
        )
    
    # variables for generate_htmlreport functions
    (
          report
        , dir_output
        , ncols
        , thumb_width
    ) = report_params

    # ------ useful message (input scales details)  ------

    # return_scl_list_from_file = (
    #   scales_lst
    # , msg_str
    # )

    # scales_lst = [
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

    # check if report has to be done and process chords
    if report != 'only':
        # main function call
        (  process_scales_msg_str
         , svg_file_path_list
         , png_file_path_list
         ) = scales2files.process_scales_file(
            input_sclf, 
            *process_scales_params
           )
    if report != 'disable':
        file_exts = ('.svg', '.png')
        htmlreport.generate_htmlreport(dir_output, file_exts, ncols, thumb_width)

    footer = "====================="
    print(footer)
    
    return process_scales_msg_str, svg_file_path_list, png_file_path_list



if __name__ == "__main__":
    
    
    # testing pad_scales and trunk_scales functions
    
    in_frets = [
          ['5', 'x', 'x', '8']
        , ['5', 'x', 'x', '8']
        , ['5', 'x', '7', '8']
        , ['5', 'x', '7', 'x']
        , ['5', '6', '7', 'x']
        , ['5', 'x', 'x', '8']
        ]
    
    in_intervals = [
          ['R', 'x', 'x',  'b3']
        , ['5', 'x', 'x',  'b7']
        , ['b3', 'x', '4', 'b5']
        , ['b7', 'x', 'R',  'x']
        , ['4', 'b5', '5',  'x']
        , ['R', 'x',  'x', 'b3']
        ]
    
    in_dlabels = [
          ['1', 'x', 'x', '4']
        , ['1', 'x', 'x', '4']
        , ['1', 'x', '3', '4']
        , ['1', 'x', '3', 'x']
        , ['1', '2', '3', 'x']
        , ['1', 'x', 'x', '4']
        ]

    out_frets, out_intervals, out_dlabels = trunk_scales(in_frets, in_intervals, in_dlabels, 5, 7)
    print('\n*** trunked frets ************')
    for strng in out_frets: print(strng)
    print('*** trunked intervals ********')
    for intrv in out_intervals: print(intrv)
    print('*** trunked dlabels **********')
    for dlbl in out_dlabels: print(dlbl)

    out_frets, out_intervals, out_dlabels = pad_scales(in_frets, in_intervals, in_dlabels, 3, 10)
    print('*** padded frets ************')
    for strng in out_frets: print(strng)
    print('*** padded intervals ********')
    for intrv in out_intervals: print(intrv)
    print('*** padded dlabels **********')
    for dlbl in out_dlabels: print(dlbl)
    

    # testing process_chords_by_config_json / process_chordsfile_by_config_json functions
      
    json_file_path = '../tests/json_cfg_tests_files/config_caged_chords.json'   # json config file path
    
    input_crdf = '../tests/crds_test_files/chord-list.txt'   # path for chord list txt
    crd_list = chord_parser.get_crd_list_from_file(input_crdf, print_output=True)[0]
    
    process_chords_by_config_json(
          json_file_path , crd_list
        , dir_output = '../dirout/chords1'
        , thumb_width = '150.0px'
        )

    input_crdf = '../tests/crds_test_files/caged_chords.txt'   # path for chord list txt
    process_chordsfile_by_config_json(
          json_file_path , input_crdf
        , dir_output = '../dirout/chords2'
        )
    
    
    # testing functions:
    # generate_scale / generate_scale_file / 
    # process_scales_by_config_json / process_scalesfile_by_config_json  

    scale_file = '../dirout/scales/myscale1.txt'
    # my_scale = (root_note, scale_name, frets, intervls, notes)
    my_scale = generate_scale('G', 'mixolydian', 16)
    dir_out = os.path.dirname(scale_file)
    generate_scale_file(my_scale, scale_file, False)
    scl_list = scale_parser.get_scales_list_from_file(scale_file, print_output=True)[0]
    
    # input variables    
    json_file_path = '../tests/json_cfg_tests_files/config_scales.json'   # json config file path
    process_scales_by_config_json(
          json_file_path , scl_list
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        , ncols = 1
        )

    scale_file = '../dirout/scales/myscale2.txt'
    # my_scale = (root_note, scale_name, frets, intervls, notes)
    my_scale = generate_scale('A', 'minor_blues_scale', 16)
    dir_out = os.path.dirname(scale_file)
    generate_scale_file(my_scale, scale_file, False)
    
    # input variables    
    json_file_path = '../tests/json_cfg_tests_files/config_scales.json'   # json config file path
    process_scalesfile_by_config_json(
          json_file_path , scale_file
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        , ncols = 1
        )


    # testing some function combinations
    
    # expand my_scale (complete neck scale) from above
    root_note, scale_name, frets, intervls, notes = my_scale
    
    # change None to 'x' and number to strings
    # ie: [[None,  1,   None,  3,  None ...], ...] -> [['x',  '1',   'x',  '3',  'x' ...], ...]
    frets_str =    [[str(elem) if elem is not None else 'x' for elem in strng] for strng in frets]
    intervls_str = [[str(elem) if elem is not None else 'x' for elem in strng] for strng in intervls]
    notes_str =    [[str(elem) if elem is not None else 'x' for elem in strng] for strng in notes]    
    
    # -- G caged form --
    # apply trunk_scales() and pad_scales()
    tr_frets, tr_intervals, tr_notes = trunk_scales(frets_str, intervls_str, notes_str, 2, 6)
    pd_frets, pd_intervals, pd_notes = pad_scales(tr_frets, tr_intervals, tr_notes, 0, 16)
    
    scale_file = '../dirout/scales/myscale_gform.txt'
    # rewrite my_scale with trunked and padded frets, intervals and notes
    my_scale = (root_note, scale_name + ' gform', pd_frets, pd_intervals, pd_notes)
    dir_out = os.path.dirname(scale_file)
    generate_scale_file(my_scale, scale_file, False)
      
    json_file_path = '../tests/json_cfg_tests_files/config_scales.json'   # json config file path
    process_scalesfile_by_config_json(
          json_file_path , scale_file
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        , ncols = 1
        , scale_label_isbottom = True
        , scale_label_isleft = True
        )
    
    # -- C caged form --
    tr_frets, tr_intervals, tr_notes = trunk_scales(frets_str, intervls_str, notes_str, 9, 13)
    pd_frets, pd_intervals, pd_notes = pad_scales(tr_frets, tr_intervals, tr_notes, 0, 16)
    
    scale_file = '../dirout/scales/myscale_cform.txt'
    my_scale = (root_note, scale_name + ' cform', pd_frets, pd_intervals, pd_notes)
    dir_out = os.path.dirname(scale_file)
    generate_scale_file(my_scale, scale_file, False)
     
    json_file_path = '../tests/json_cfg_tests_files/config_scales.json'   # json config file path
    process_scalesfile_by_config_json(
          json_file_path , scale_file
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        , ncols = 1
        , scale_label_isbottom = True
        , scale_label_isleft = True
        )