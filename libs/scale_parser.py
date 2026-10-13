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
scale_parser: read and validate scale files for fancyscales.

A scale file is a sequence of blocks, one per scale. Every block has 11
lines, always in this order (tab separated, '//' starts a comment line):

    NAME        scale label ('\\n' gives a 2 lines label)
    FOLDER      output subfolder, '%' for none
    FILENAME    file name without extension, '%' to derive it from NAME
    STRING01    frets <tab> intervals <tab> dlabels   (1st string, high e)
    ...
    STRING06    frets <tab> intervals <tab> dlabels   (6th string, low E)
    FOOTER      up to 6 labels under the fretboard, '%' for none
    ARROWS      python tuple of arrows, ie ( ((5,2), (8,2)), ), '%' for none

Every STRING line holds comma separated lists with one element per fret
column, 'x' where there is no note, ie: 'x,8,x,10,11'. All 6 strings must
have the same number of columns.

Functions, from file to validated scale list:
    parse_scales_from_file()    check the block structure, return raw dicts
    get_scales_list()           validate every scale with check_scl_params()
    get_scales_list_from_file() both steps, used by scales2files
"""

# standard imports
import ast

# local application imports
from libs import global_constants
from libs import global_utilities


# scale file line elements for each scale (all must exist)
scale_file_blocks = (
      'NAME'
    , 'FOLDER'
    , 'FILENAME'
    , 'STRING01'
    , 'STRING02'
    , 'STRING03'
    , 'STRING04'
    , 'STRING05'
    , 'STRING06'
    , 'FOOTER'
    , 'ARROWS'
    )


def check_scale_fretlist_correct(fretlist):
    '''
    check if frets string is correct
    ie:
    - number of elements must be >=3 
    - all elements are numbers between 0 and 24
      or, if char, only 'x' or 'X'
    
    Note: 
    - 'String' with capital   'S' refer to guitar string
    - 'string' with lowercase 's' refer to python variable type
    
    fretlist: List of strings, fret sequence for a single String
              ie: ['x', '3', '2', '0', '1', '0']
    
    return boolean correct variable
    '''
    correct = True
    if len(fretlist) < 3:
        correct = False
    else:
        for el in fretlist:
            if el.isdigit():
                el_int = int(el)
                correct = correct and ((el_int >= 0) and (el_int <= 24))
            else:
                correct = correct and (el.lower() == 'x')
    return correct


def check_scale_arrowslist_correct(arrowslist):
    '''
    check if arrowslist list is correct
    - arrowslist must be a list of tuple. Each tuple is a 2-tuple of 2-tuple
      representing a start point and an end point ((Fret1, String1), (Fret2, String2))
      ie: arrowslist = [((5,6), (8,6)), ((7,9), (2,5))]
    - all elements represent points (FretX, StringY) so they have to be integers
    - these integers must be between 0 and 24
    
    arrowslist: List of 2-tuple of 2-tuple representing an arrows sequence
                [(arrow1), (arrow2), (arrow3), ...] =
                [(start_point1, end_point1), (start_point2, end_point2), ...] =
                [((start_Fret1, start_String1), (end_Fret1, end_String1)), ((start_Fret2, start_String2), ...]
    
    return boolean correct variable
    '''

    correct = False
    
    # example: arrowslist = [((5,6), (8,6)), ((7,9), (2,5))]

    # check all arrowslist elements are tuples (if arrowslist is not Null)
    chk_all_tuples_lvl1 = all(type(elem) is tuple for elem in arrowslist) if arrowslist else False
    # print(chk_all_tuples_lvl1)
    if chk_all_tuples_lvl1:
        # lens_arrowslist_lvl1 = [2, 2]
        lens_arrowslist_lvl1 = [len(elem) for elem in arrowslist]
        # print(lens_arrowslist_lvl1)
        # check len is 2 for each element
        chk_all_lens_lvl1 = all((elem==2) for elem in lens_arrowslist_lvl1)
        # print(chk_all_lens_lvl1)
        if chk_all_lens_lvl1:
            # flatted_arrowslist_lvl1 = [(5, 6), (8, 6), (7, 9), (2, 5)]
            flatted_arrowslist_lvl1 = [subelem for elem in arrowslist for subelem in elem]
            # print(flatted_arrowslist_lvl1)
            # check all flatted_arrowslist_lvl1 elements are tuples
            chk_all_tuples_lvl2 = all(type(elem) is tuple for elem in flatted_arrowslist_lvl1)
            # print(chk_all_tuples_lvl2)
            if chk_all_tuples_lvl2:
                lens_arrowslist_lvl2 = [len(elem) for elem in flatted_arrowslist_lvl1]
                # print(lens_arrowslist_lvl2)
                # check len is 2 for each element
                chk_all_lens_lvl2 = all((elem==2) for elem in lens_arrowslist_lvl2)
                # print(chk_all_lens_lvl2)
                if chk_all_lens_lvl2:
                    # flatted_arrowslist_lvl2 = [5, 6, 8, 6, 7, 9, 2, 5]
                    flatted_arrowslist_lvl2 = [subelem for elem in flatted_arrowslist_lvl1 for subelem in elem]
                    # print(flatted_arrowslist_lvl2)
                    # check each element is an integer
                    chk_flatted_arrowslist_isint = all(isinstance(elem, int) for elem in flatted_arrowslist_lvl2)
                    # print(chk_flatted_arrowslist_isint)
                    if chk_flatted_arrowslist_isint:
                        # check each integer is >= 0 and <= 24
                        chk_frets = all(((elem >= 0) and (elem <= 24)) for elem in flatted_arrowslist_lvl2)
                        # print(chk_frets)
                        # if all above conditions are satisfied correct = True
                        correct = chk_frets
    
    return correct



def check_strngs_params(
          string_01
        , string_02
        , string_03
        , string_04
        , string_05
        , string_06
        ):
    '''
    check if 6 Strings parameters are correct and return also
    Strings list, Frets list and Dlabels list. 
    Each string parameter is a list of lists, like
    string_0x = [[frets_0x], [intervals_0x], [dlabels_0x]]
    where [frets_0x] =     ['x', '8', 'x', '10' ..]
          [intervals_0x] = ['x', 'R', 'x', 'b5' ..]
          ...
    
    Note: 
    - 'String' with capital   'S' refer to guitar string
    - 'string' with lowercase 's' refer to python variable type
    
    These are the rules:
    --------------------
    
    - All 6 Strings Fret sequences must have same lenght
      ie: string_01 = [['x', '8', 'x', '10', '11'], [..]]
          string_02 = [['7', 'x', 'x', '10', 'x' ], [..]]
          ...
          is OK
          string_01 = [['x', '8', 'x', '10', '11'],[..]]
          string_02 = [['5', 'x', 'x', '8'       ],[..]]
          ...
          is KO   
    
    - All 6 Strings Intervals sequences must have same lenght
      ie: string_01 = [[..], ['x', 'b3', 'x', '4' , 'b5'], [..]]
          string_02 = [[..], ['5', 'x' , 'x', 'b7', 'x' ], [..]]
          ...
          is OK
          string_01 = [[..], ['b3', 'x',  '4' , 'b5'      ], [..]]
          string_02 = [[..], ['5',  'x' , 'x',  'b7', 'x' ], [..]]
          ...
          is KO   

    - Intervals sequences and DLabels sequences are optional but if they exist 
      * all 6 Strings must have their own Interval/Dlabels sequence
      * number of Interval sequences must be equal to number of Fret sequences
      * number of DLabels sequences must be equal to number of Fret sequences
      ie: string_01 = [['x', '8', 'x', '10', '11'], ['x', 'b3', 'x', '4 ', 'b5'], ['x', '1', 'x', '3', '4']]
          string_02 = [['7', 'x', 'x', '10', 'x '], ['5', 'x ', 'x', 'b7', 'x' ], ['1', 'x', 'x', '4', 'x']]
          ...
          is OK
          string_01 = [['x', '8', 'x', '10', '11'], [..], [..]]
          string_02 = [['7', 'x', 'x', '10', 'x '], [..], [..]]
          ...
          is OK
          string_01 = [['x', '8', 'x', '10', '11'], ['x', 'b3', 'x '], [..]]
          string_02 = [['5', 'x', 'x', '8'],        ['5', 'x ', 'x '], [..]]
          ...
          is KO
          string_01 = [['x', '8', 'x', '10', '11'], ['x', 'b3', 'x', '4 ', 'b5'], ['x', '1', 'x']]
          string_02 = [['7', 'x', 'x', '10', 'x '], ['5', 'x ', 'x', 'b7', 'x' ], ['1', 'x', 'x']]
          ...
          is KO
      
    - Minimum String frets list lenght is 3, 
      ie: string_0X = [['1', 'x', '3'], [..]] is OK
          string_0X = [['1', '2'],      [..]] is KO
        
    string_0x: 
        List of 3 lists -> [
              xth-String fret sequence (as a single text string)
            , xth-String intervals sequence (as a single text string)
            , xth-String dlabels sequence (as a single text string)
        ]
        ie: string_06 =  [
              ['x', '8',  'x', '10', '11']
            , ['x', 'b3', 'x', '4',  'b5']
            , ['x', '1',  'x', '3',  '4']
            ] means that on String 6:
        * fingered frets are 8,10,11
        * these correspond to b3,4,b5 intervals.
        * finger numbers are 1,3,4
        
    return tuple of parameters: (
          error_in_scale: message String
        , error_message: message String
        , strgs_frets_list: list of lists (6 elements, one for every guitar String - frets positions)
        , strgs_intervals_list: list of lists (6 elements, one for every guitar String - intervals positions), optional
        , strgs_dlabels_list: list of lists (6 elements, one for every guitar String - dlabels positions), optional
        )

    ie: (
          True
        , 'error in intervals syntax, ...'
        , [
              ['5', 'x', 'x', '8'], ['5', '6', '7', 'x'], ['5', 'x', '7', 'x'], ['5', 'x', '7', '8']
            , ...
          ]
        , [
              ['R', 'x', 'x', 'b3'], ['4', 'b5', '5', 'x'], ['b7', 'x', 'R', 'x'], ['b3', 'x', '4', 'b5']
            , ...
        ]
        , [
              ['1', 'x', 'x', '4'], ['1', '2', '3', 'x'], ['1', 'x', '3', 'x'], ['1', 'x', '3', '4']
            , ...
        ]
        ) 
    '''
    
    # error flag for chord syntax
    error_in_scale = False
    # error message in case of errors
    error_message = '' 
    
    # stringelements_split_list=  : [[['x', '8', 'x', '10', '11'], ['x', 'b3', 'x', '4', 'b5'], ['x', '1', 'x', '3', '4']], 
    #                            [['7', 'x', 'x', '10', 'x'], ['5', 'x', 'x', 'b7', 'x'], ['1', 'x', 'x', '4', 'x']], ... ]
    stringelements_split_list =  [string_01, string_02, string_03, string_04, string_05, string_06]
    
    # ======== Strings lenghts check ========
    
    # frets list: strgs_frets_list = [['x', '8', 'x', '10', '11'], ['7', 'x', 'x', '10', 'x'], ...]
    strgs_frets_list = [s[0] for s in stringelements_split_list]
    # interval list: strgs_intervals_list = [['x', 'b3', 'x', '4', 'b5'], ['5', 'x', 'x', 'b7', 'x'], ...]
    strgs_intervals_list = [l[1] for l in stringelements_split_list if (len(l)>1 and l[1])]
    # dlabel list: strgs_dlabels_list = [['x', '1', 'x', '3', '4'], ['1', 'x', 'x', '4', 'x'],  ...]
    strgs_dlabels_list = [k[2] for k in stringelements_split_list if (len(k)>2 and k[2])]
    
    # frets lenght list: [5, 5, 5, 5, 5, 5]
    strgs_frets_len_list = [len(s) for s in strgs_frets_list]
    # intervals lenght list: [5, 5, 5, 5, 5, 5]
    strgs_intervals_len_list = [len(l) for l in strgs_intervals_list]
    # dlabels lenght list: [5, 5, 5, 5, 5, 5]
    strgs_dlabels_len_list = [len(k) for k in strgs_dlabels_list]
    
    # check if all elements of lists (Strings, Intervals, DLabels) have the same lenght
    # all() function returns True if all items in an iterable are true, otherwise it returns False.
    chk_frets_all_same_len = all((elem == strgs_frets_len_list[0]) for elem in strgs_frets_len_list)
    chk_intervals_all_same_len = all((elem == strgs_intervals_len_list[0]) for elem in strgs_intervals_len_list)  
    chk_dlabels_all_same_len = all((elem == strgs_dlabels_len_list[0]) for elem in strgs_dlabels_len_list)
    
    if (not chk_frets_all_same_len):
        error_in_scale = True
        error_message += 'frets elements are not all of same lenght;'
    if (not chk_intervals_all_same_len):
        error_in_scale = True
        error_message += 'interval elements are not all of same lenght;'   
    if (not chk_dlabels_all_same_len):
        error_in_scale = True
        error_message += 'dlabels elements are not all of same lenght;' 
    
    # if Intervals list exist check if every String has its own intervals and dlabels list
    # get frets, interval and dlables list lenghts
    len_strgs_frets_list = len(strgs_frets_list)
    len_strgs_intervals_list = len(strgs_intervals_list)
    len_strgs_dlabels_list = len(strgs_dlabels_list)
    
    chk_1fret_1interv = True if (len_strgs_frets_list == len_strgs_intervals_list) else False
    chk_1fret_1dlabel = True if (len_strgs_frets_list == len_strgs_dlabels_list) else False
    
    # if intervals lenght lists exist check len fret is equal to len intervals
    if (not chk_1fret_1interv) and len_strgs_intervals_list:
        error_in_scale = True
        error_message += 'some string has not its own intervals defined or viceversa;'
    # if dlabels lenght lists exist check len fret is equal to len dlabels
    if (not chk_1fret_1dlabel) and len_strgs_dlabels_list:
        error_in_scale = True
        error_message += 'some string has not its own dlabels defined or viceversa;'
 
    # if Intervals and Frets lists exist and all elements of lists (Strings, Intervals) have the same lenght
    # then check if this lenght is the same for the two lists
    if len_strgs_intervals_list and len_strgs_frets_list:
        if chk_frets_all_same_len and chk_intervals_all_same_len:
            if strgs_frets_len_list[0] != strgs_intervals_len_list[0]:
                error_in_scale = True
                error_message += 'frets and interval elements are not all of same lenght;'
    # if Frets and DLabels lists exist and all elements of lists (Strings, DLabels) have the same lenght
    # then check if this lenght is the same for the two lists.
    # note: this must not depend on intervals (it used to check
    # len_strgs_intervals_list, so a scale with dlabels but without
    # intervals was never checked)
    if len_strgs_dlabels_list and len_strgs_frets_list:
        if chk_frets_all_same_len and chk_dlabels_all_same_len:        
            if strgs_frets_len_list[0] != strgs_dlabels_len_list[0]:
                error_in_scale = True
                error_message += 'frets and dlabels elements are not all of same lenght;'


    # ========  worng frets chars and min frets lenght check ========
    
    check_allscales_fretlist_correct = all(check_scale_fretlist_correct(elem) for elem in strgs_frets_list)
    if not check_allscales_fretlist_correct:
        error_in_scale = True
        error_message += 'error in fretlist: worng chars or number of frets must be at least 3;'


    # ======== check intervals chars are valid ========
    
    for intervals in strgs_intervals_list:    
        if (not set(intervals).issubset(global_constants.intervals_set_allowed_chars)):
            error_in_scale = True
            error_message += 'error in intervals syntax;'
            # break otherwise error message is too long and repetitive
            break
    
    return (
          error_in_scale
        , error_message
        , strgs_frets_list
        , strgs_intervals_list
        , strgs_dlabels_list
        )



def check_scl_params(
          scale_name
        , subfolder
        , filename
        , string_01
        , string_02
        , string_03
        , string_04
        , string_05
        , string_06
        , footer
        , arrows
        ):
    '''
    check if all scale main parameters are correct and return them splitted in lists.
    
    scale_name: String, scale name ie: 'Am Blues Scale'
    subfolder: String, subfolder path ie: './mysub/'
    filename: String, scale file name
    string_0x: 
        List of 3 strings -> [
              xth-String fret sequence (as a single text string)
            , xth-String intervals sequence (as a single text string)
            , xth-String dlabels sequence (as a single text string)
        ]
        ie: string_06 =  ['x,8,x,10,11', 'x,b3,x,4,b5, 'x,1,x,3,4'] means that on String 6:
        * fingered frets are 8,10,11
        * these correspond to b3,4,b5 intervals.
        * finger numbers are 1,3,4
    footer: String, footer string ie: 'E,A,D,G,B,e'
    arrows: String, arrows string ie: '( ((5,2), (8,2)), ((5,4), (7,4)), ((6,5), (7,5)) )'
    
    
    return tuple of parameters: (
          error_in_scale: message String
        , error_message: message String
        , scale_filename: String, scale filename
        , subfolder: String, scale subfolder
        , strgs_frets_list: list of lists (6 elements, one for every guitar String - frets positions)
        , strgs_intervals_list: list of lists (6 elements, one for every guitar String - intervals positions), optional
        , strgs_dlabels_list: list of lists (6 elements, one for every guitar String - dlabels positions), optional
        , footer: list of strings (6 elements, one for every guitar String - footers), optional
        , arrows_list: list of tuples for arrows, ie [ ((5,2), (8,2)), ( ... ]
        )

    ie: (
          True
        , 'error in intervals syntax, ...'
        , 'Am_Blues_Scale_Position_1'
        , './Blues_Scale/'
        , [
              ['5', 'x', 'x', '8'], ['5', '6', '7', 'x'], ['5', 'x', '7', 'x'], ['5', 'x', '7', '8']
            , ...
          ]
        , [
              ['R', 'x', 'x', 'b3'], ['4', 'b5', '5', 'x'], ['b7', 'x', 'R', 'x'], ['b3', 'x', '4', 'b5']
            , ...
        ]
        , [
              ['1', 'x', 'x', '4'], ['1', '2', '3', 'x'], ['1', 'x', '3', 'x'], ['1', 'x', '3', '4']
            , ...
        ]
        , ...
        , ['E', 'A', 'D', 'G', 'B', 'e']
        , [ ((5,2), (8,2)), ((5,4), (7,4)), ((6,5), (7,5)) ]
        ) 
    '''
    
    # ======== scale_name and scale_filename elaboration ========
    
    scale_postfix = ''
    # if a '.' is in scale name then use what string is after that
    # '.' for a postfix in scale file name. Only first '.' from left
    # count for splitting. 
    # scale_postfix can be used below if filename is not given
    if scale_name.count('.') >= 1: (scale_name, scale_postfix) = scale_name.split('.', 1)
    
    # if '\n' is present in scale_name then change it to newline
    if '\\n' in scale_name: scale_name = scale_name.replace('\\n', '\n')
    
    # filename is given, then sanitize it and assign it to scale_filename.
    # '%' means "not given" (like in the other fields): without this check
    # sanitize_str('%') returned '' and the image was saved as '.svg'
    if filename and filename.strip() != '%':
        scale_filename = global_utilities.sanitize_str(filename)
    # else derive scale_filename from scale_name (use also 
    # scale_postfix from above)
    else:
        scale_filename = scale_name + '.' + scale_postfix if scale_postfix else scale_name
        # sanitize scale_filename
        scale_filename = global_utilities.sanitize_str(scale_filename)
            

    # ======== check if subfolder is null or only whitespaces ======== 
    
    if subfolder.strip():
        # if it is be a single '%' then reset
        if (subfolder == '%'):
            subfolder = ''
        else:
            subfolder = subfolder.strip() + '/'
    else:
        subfolder = ''    

    
    # ======== preparing Strings check ========
    
    # scale_name, subfolder, string_01, .. = 'Am Blues Scale, Position 2', './Blues_Scale/', ['x,1,x,3,4', 'x,b3,x,4,b5'], ..
    # stringelements_list = [['x,8,x,10,11', 'x,b3,x,4,b5', 'x,1,x,3,4'], ['7,x,x,10,x', '5,x,x,b7,x', '1,x,x,4,x'], ... ]
    # stringelements_split_list=  : [[['x', '8', 'x', '10', '11'], ['x', 'b3', 'x', '4', 'b5'], ['x', '1', 'x', '3', '4']], 
    #                            [['7', 'x', 'x', '10', 'x'], ['5', 'x', 'x', 'b7', 'x'], ['1', 'x', 'x', '4', 'x']], ... ]
    stringelements_list = [string_01, string_02, string_03, string_04, string_05, string_06]
    stringelements_split_list = []
    for strings in stringelements_list:
        new_string = []
        for string in strings:
            if string:
                # if string is a '%' append empty list
                if string == '%':
                    new_string.append([])
                else:
                    # 'x,8,x,10,11' -> crd_str2slst -> ['x', '8', 'x', '10', '11']
                    # 'x,1,x,3,4'   -> crd_str2slst -> ['x', '1', 'x', '3', '4']
                    new_string.append(global_utilities.crd_str2slst(string))
            else:
                new_string.append([])
        if new_string: stringelements_split_list.append(new_string)
    
    # ======== Strings check ========
    # Strings check using check_strngs_params function
    # where:
    # strgs_frets_list =     [['x', '8',  'x', '10', 'x' ], ['7', '8',  '9', 'x', 'x'], ...]
    # strgs_intervals_list = [['x', 'b3', 'x', '4',  'b5'], ['x', 'b7', 'x', 'R', 'x'], ...]
    # strgs_dlabels_list =   [['x', '1',  'x', '3',   '4'], ['x', '1',  'x', '3', 'x'], ...]
    ( error_in_scale
    , error_message
    , strgs_frets_list
    , strgs_intervals_list
    , strgs_dlabels_list) = check_strngs_params(*stringelements_split_list)
            

    # ======== footer checks ========
    
    # check if footer is null or only whitespaces
    # and also is not a '%'
    if footer.strip() and (footer != '%'):
        # split footer string in a list and remove whitespaces
        # from every single footer label
        footer = global_utilities.crd_str2slst(footer)
        # if a footer elem has more than 3 chars then it is an error
        # (every element is checked, not only the first one)
        if any(len(elem) > 3 for elem in footer):
            error_in_scale = True
            error_message += 'error in footer syntax no more of 3 chars allowed per element '
        # if footer has more than 6 elements then it is an error
        elif (len(footer) > 6):
            error_in_scale = True
            error_message += 'error in footer syntax no more of 6 elements are allowed '    
    else:
        footer = []


    # ======== arrows checks ========
    
    # check if arrows is null or only whitespaces
    # and also is not a '%'
    arrows_list = []
    if arrows.strip() and (arrows != '%'):
        try:
            # get a tuple from a string (ast built-in module)
            arrows_tuple = ast.literal_eval(arrows)
            # check for tuple type
            if type(arrows_tuple) is tuple:
                # convert to list
                arrows_list = list(arrows_tuple)
                # check if every arrows_list is correct (see check_scale_arrowslist_correct() above)
                if not check_scale_arrowslist_correct(arrows_list):
                    error_in_scale = True
                    error_message += 'error in arrows syntax  '                            
            else:
                error_in_scale = True
                error_message += 'error in arrows syntax  ' 
        # literal_eval raises different exceptions for different syntax errors
        # (ValueError, SyntaxError, ...): all of them mean wrong arrows
        except Exception:
            error_in_scale = True
            error_message += 'error in arrows syntax  ' 
    
    
    return (
          error_in_scale
        , error_message
        , scale_name
        , scale_filename
        , subfolder
        , strgs_frets_list
        , strgs_intervals_list
        , strgs_dlabels_list
        , footer
        , arrows_list
        )


def get_scales_list(scales_lst, print_output=True):
    '''
    take scales_lst (a list of dicts where each dict is a scale) and check 
    if scales are correct and return them as a list of list, each list is a scale.
    output list single element structure is:
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
        ]
    
    scales_lst: list of dicts. Structure is:
    [
        {
            'scale_name': string, ie: 'Am Blues Scale, Position 1'
          , 'subfolder': string, ie: './Blues_Scale/'
          , 'scale_filename':string, ie: 'Am_Blues_Scale__Position_2'
          , 'string0x': list of 3 strings, [frets, intervals, dlabels] ie: ['5,x,x,8', 'R,x,x,b3', '1,x,x,4']
          , ...
          , 'footer': 'E,A,D,G,B,e'
          , 'arrows': '((5,6), (8,6)), ...'
        }, ..
    ]
        
    return tuple of parameters: (
      scales_lst
    , msg_str
    )
    
    ie: 
    (
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
            ]
            , [
            ...
            ]
        ]
        , 'Getting Scales from File ...'
    )
    '''
    msg_str = ''
    scl_list = []
    header = 'Checking scales syntax' + '\n======================'
    if print_output: print(header)
    msg_str += header + '\n'
    # scales_lst = [{scale1dict}, {scale2dict}, ..]
    # scalexdict = {'scale_name':'Am Blue..', ..., 'string01':['5,x,x,8',...]...,  }   
    for scale in scales_lst:
        # check if all scale main parameters are correct 
        # and return them splitted in lists
        (
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
         ) = check_scl_params(
                scale['scale_name'], 
                scale['subfolder'], 
                scale['scale_filename'],
                scale['string01'], 
                scale['string02'], 
                scale['string03'], 
                scale['string04'], 
                scale['string05'], 
                scale['string06'],
                scale['footer'],
                scale['arrows']
            )
        if error_in_scale:
            error_msg = ' | '.join([elem for elem in error_message.split(';') if elem])
            ko_str = '- ' + scale_filename + ': KO\n  ' + error_msg
            msg_str += ko_str + '\n'
            if print_output: print(ko_str)
        else:
            ok_str = '- ' + scale_filename + ': OK'
            msg_str += ok_str + '\n'
            if print_output: print(ok_str)
            scl_list.append(
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
                ]
            )
    
    # make every output file name unique (ie two scales with the same name
    # would overwrite each other): Am, Am -> Am, Am.v02.
    # scale_filename is element 3 of every scale list
    global_utilities.fix_duplicate_filenames(scl_list, 3)
            
    return (scl_list, msg_str)


def parse_scales_from_file(input_sclf, print_output=True):
    '''
    process scales txt file and return a list. 
    Last element of this list is a list of dicts, each dict is a scale.
    dict structure is:
        {
           'scale_name': string, ie: 'Am Blues Scale, Position 1'
          , 'subfolder': string, ie: './Blues_Scale/'
          , 'scale_filename':string, ie: 'Am_Blues_Scale__Position_2'
          , 'string0x': list of 3 strings, [frets, intervals, dlabels] ie: ['5,x,x,8', 'R,x,x,b3', '1,x,x,4']
          , ...
          , 'footer': 'E,A,D,G,B,e'
          , 'arrows': '((5,6), (8,6))'
        }
    scale file must have a strict structure: each scale must have 10 elements (see example file):
        NAME, FOLDER, FILENAME, STRING01, STRING02, STRING03, STRING04, STRING05, STRING06, FOOTER, ARROWS
    this function checks if all elements are present for each scale in correct order
    
    return list of parameters: [
      error_in_file
    , msg_str
    , scales_lst
    ]
    
    ie: 
          'False'
        , 'Getting Scales ....'
        , [
              {
               'scale_name': 'Am Blues Scale, Position 2'
              , 'subfolder': './Blues_Scale'
              , 'filename': 'Am_Blues_Scale2'
              , 'string01': ['x,8,x,10,11', 'x,b3,x,4,b5', 'x,1,x,3,4']
              , 'string02': ['7,x,x,10,x', '5,x,x,b7,x', '1,x,x,4,x']
              , ...
              , 'footer': 'E,A,D,G,B,e'
              , 'arrows': '((5,6), (8,6))'
            }
            , {
                'scale_name': 'Am Blues Scale, Position 1'
              , 'subfolder': ''
              , 'filename': ''
              , 'string01': ['5,x,x,8', 'R,x,x,b3', '1,x,x,4']
              , 'string02': ['5,6,7,x', '4,b5,5,x', '1,2,3,x']
              , ...
              , 'footer': ''
              , 'arrows': ''
            }
        ]
    '''
    # global bool var for error in file structure 
    error_in_file = False
    # useful error message
    error_message = ''
    # text file linenumber where error is (approximately)
    error_line = 0
    # block counter (each scale has its block), it can be used to count how many scales are in the file
    block_number = 0
    # current linemunber
    linenumber = 0
    # current element of each block
    block_elem_index = 0
    # scales_lst = [{dict scale1}, {dict scale2}, ...]
    scales_lst = []
    
    # variables initialization
    scale_name = ''
    subfolder = None
    scale_filename = None
    # ie, for String 05 we have: 
    # frets_strng05='x,8,x,10,x', intrvls_strng05='x,b7,x,R,x', dlabels_strng05 = 'x,1,x,3,x'
    frets_strng01, intrvls_strng01, dlabels_strng01 = '', '', ''
    frets_strng02, intrvls_strng02, dlabels_strng02 = '', '', ''
    frets_strng03, intrvls_strng03, dlabels_strng03 = '', '', ''
    frets_strng04, intrvls_strng04, dlabels_strng04 = '', '', ''
    frets_strng05, intrvls_strng05, dlabels_strng05 = '', '', ''
    frets_strng06, intrvls_strng06, dlabels_strng06 = '', '', ''
    footer = None
    arrows = None
    
    header = '\nGetting Scales from File\n========================\n' + \
             'Processing scales file: ' + input_sclf
    msg_str = header
    if print_output: print(header)
    
    # utf-8 on every OS ('utf-8-sig' also removes the BOM some Windows editors add)
    with open(input_sclf, mode='r', encoding='utf-8-sig') as infile:
        
        for infile_line in infile:
            
            linenumber += 1
            if error_in_file: break
            # strip start and final spaces
            infile_line_strip = infile_line.strip()
            # strip empty lines, newlines and comments (//)
            if (not infile_line_strip) or (infile_line_strip[0:2] == '//'): continue
            # make listelem list by tabs splitting
            # ie: listelem = ['STRING0X', 'x,8,x,10,11', 'x,b3,x,4,b5', 'x,1,x,3,4'] 
            #             or ['NAME', 'Am Blues Scale..']
            listelem = infile_line_strip.split('\t')
            # strip empty elements (nulls or whitespaces)
            listelem = [x for x in listelem if x.strip()]
            len_listelem = len(listelem)
            
            # check if line is an allowed block
            if listelem[0] not in scale_file_blocks:
                error_in_file = True
                error_message += 'unknown line, '
                error_line = linenumber  
            
            # if line is NAME block check if preceding block is complete (block_elem_index=0)
            # if not report error linenumber
            if listelem[0] == 'NAME':
                if block_elem_index > 0:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:  
                    # check if name string exist (2nd element of listelem)
                    if len_listelem == 2:
                        scale_name = listelem[1]
                    else:
                        error_in_file = True
                        error_message += 'error in name element, '
                        error_line = linenumber
                        
            # if line is subfolder block check if it is 2nd scale block (block_elem_index=1)
            # if not report error linenumber
            if listelem[0] == 'FOLDER':
                if block_elem_index != 1:
                    error_in_file = True
                    error_message += 'scale block missing / not closed '
                    error_line = linenumber - 1
                else:
                    # check if subfolder string exist (2nd element of listelem)
                    if (len_listelem == 2): 
                        subfolder = listelem[1]
                    else:
                        subfolder = ''
                        
            # if line is filename block check if it is 3nd scale block (block_elem_index=2)
            # if not report error linenumber
            if listelem[0] == 'FILENAME':
                if block_elem_index != 2:
                    error_in_file = True
                    error_message += 'scale block missing / not closed '
                    error_line = linenumber - 1
                else:
                    # check if subfolder string exist (2nd element of listelem)
                    if (len_listelem == 2): 
                        scale_filename = listelem[1]
                    else:
                        scale_filename = ''

            # if line is STRING01 block check if it is 3nd scale block (block_elem_index=3)
            # if not report error linenumber
            if listelem[0] == 'STRING01':
                if block_elem_index != 3:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:
                    # if listelem has only 1 elem then there are no frets neither intervals
                    # listelem = ['STRING0X', 'x,1,x,3,4', 'x,b3,x,4,b5']
                    if (len_listelem < 2):
                        error_in_file = True
                        error_message += 'error in string01 element, '
                        error_line = linenumber        
                    else:     
                        # if frets exist it is 2nd elem
                        if (len_listelem >= 2): frets_strng01 = listelem[1]
                        # if intervals exist it is 3rd elem
                        if (len_listelem >= 3): intrvls_strng01 = listelem[2]
                        # if dlabels exist it is 4th elem
                        if (len_listelem >= 4): dlabels_strng01 = listelem[3]
    
            if listelem[0] == 'STRING02':
                if block_elem_index != 4:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:
                    if (len_listelem < 2):
                        error_in_file = True
                        error_message += 'error in string02 element, '
                        error_line = linenumber        
                    else:
                        if (len_listelem >= 2): frets_strng02   = listelem[1]
                        if (len_listelem >= 3): intrvls_strng02 = listelem[2]
                        if (len_listelem >= 4): dlabels_strng02 = listelem[3]
    
            if listelem[0] == 'STRING03':
                if block_elem_index != 5:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:
                    if (len_listelem < 2):
                        error_in_file = True
                        error_message += 'error in string03 element, '
                        error_line = linenumber        
                    else:
                        if (len_listelem >= 2): frets_strng03   = listelem[1]
                        if (len_listelem >= 3): intrvls_strng03 = listelem[2]
                        if (len_listelem >= 4): dlabels_strng03 = listelem[3]

            if listelem[0] == 'STRING04':
                if block_elem_index != 6:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:
                    if (len_listelem < 2):
                        error_in_file = True
                        error_message += 'error in string04 element, '
                        error_line = linenumber        
                    else:
                        if (len_listelem >= 2): frets_strng04   = listelem[1]
                        if (len_listelem >= 3): intrvls_strng04 = listelem[2]
                        if (len_listelem >= 4): dlabels_strng04 = listelem[3]
    
            if listelem[0] == 'STRING05':
                if block_elem_index != 7:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:
                    if (len_listelem < 2):
                        error_in_file = True
                        error_message += 'error in string05 element, '
                        error_line = linenumber        
                    else:
                        if (len_listelem >= 2): frets_strng05   = listelem[1]
                        if (len_listelem >= 3): intrvls_strng05 = listelem[2]
                        if (len_listelem >= 4): dlabels_strng05 = listelem[3]

            if listelem[0] == 'STRING06':
                if block_elem_index != 8:
                    error_in_file = True
                    error_message += 'scale block missing / not closed, '
                    error_line = linenumber - 1
                else:
                    if (len_listelem < 2):
                        error_in_file = True
                        error_message += 'error in string06 element, '
                        error_line = linenumber        
                    else:
                        if (len_listelem >= 2): frets_strng06   = listelem[1]
                        if (len_listelem >= 3): intrvls_strng06 = listelem[2]
                        if (len_listelem >= 4): dlabels_strng06 = listelem[3]

            # if line is FOOTER block check if it is 9nd scale block (block_elem_index=9)
            # if not report error linenumber
            if listelem[0] == 'FOOTER':
                if block_elem_index != 9:
                    error_in_file = True
                    error_message += 'scale block missing / not closed '
                    error_line = linenumber - 1
                else:
                    # check if footer string exist (2nd element of listelem)
                    if (len_listelem == 2):
                        footer = listelem[1]
                    else:
                        footer = ''

            # if line is ARROWS block check if it is 10th scale block (block_elem_index=10)
            # if not report error linenumber
            if listelem[0] == 'ARROWS':
                if block_elem_index != 10:
                    error_in_file = True
                    error_message += 'scale block missing / not closed '
                    error_line = linenumber - 1
                else:
                    # check if footer string exist (2nd element of listelem)
                    if (len_listelem == 2):
                        arrows = listelem[1]
                    else:
                        arrows = ''

            # block element is increased only if there are no errors
            if not error_in_file: 
                block_elem_index +=1
            
            # if block element is complete (so no errors, were found)
            # reset block_elem_index and increase block_number
            if block_elem_index == 11:
                block_elem_index = 0
                block_number += 1
                # then append scale dict
                scales_lst.append(
                        {
                          'scale_name': scale_name
                        , 'subfolder': subfolder
                        , 'scale_filename': scale_filename
                        , 'string01': [frets_strng01, intrvls_strng01, dlabels_strng01] 
                        , 'string02': [frets_strng02, intrvls_strng02, dlabels_strng02]
                        , 'string03': [frets_strng03, intrvls_strng03, dlabels_strng03]
                        , 'string04': [frets_strng04, intrvls_strng04, dlabels_strng04]
                        , 'string05': [frets_strng05, intrvls_strng05, dlabels_strng05]
                        , 'string06': [frets_strng06, intrvls_strng06, dlabels_strng06]
                        , 'footer': footer
                        , 'arrows': arrows
                        }
                    )    
                # reset all dict elements for next scale
                scale_name = ''
                subfolder = None
                scale_filename = None
                frets_strng01, intrvls_strng01, dlabels_strng01 = '', '', ''
                frets_strng02, intrvls_strng02, dlabels_strng02 = '', '', ''
                frets_strng03, intrvls_strng03, dlabels_strng03 = '', '', ''
                frets_strng04, intrvls_strng04, dlabels_strng04 = '', '', ''
                frets_strng05, intrvls_strng05, dlabels_strng05 = '', '', ''
                frets_strng06, intrvls_strng06, dlabels_strng06 = '', '', ''
                footer = None
                arrows = None
                
    # if after reaching end of file last block is not complete
    # then report error
    if (not error_in_file) and (block_elem_index !=0):
                error_in_file = True
                error_message += 'block not complete, '
                error_line = linenumber + 1
    
    # file structure status (it used to print 'Error in scale file: False'
    # when everything was fine, which read like an error)
    status_str = 'Scale file structure: ' + ('ERROR' if error_in_file else 'OK')
    status_str += '\nComplete scales loaded from file: ' + str(block_number)
    msg_str += '\n' + status_str + '\n'
    if print_output: print(status_str)
    
    # print each scale found
    status_str = ''
    if block_number:
        for scl in scales_lst:
            status_str +=  '- ' + str(scl['scale_name']) + '\n'
        msg_str += status_str
        if print_output: print(status_str)
    
    # print error description if any
    status_str = ''
    if error_in_file:
        status_str += 'Error in file structure!' + '\n - ' + error_message
        status_str += '\n - block_elem_index: ' +  str(block_elem_index + 1) + \
                        ' (' + scale_file_blocks[block_elem_index] + ')'
        status_str += '\n - error around line: '  + str(error_line)
        status_str += '\n - last elemets\' dump: \n\t'
        status_str += 'scale_name: ' + scale_name + '\n\t'
        status_str += 'scale_filename: ' + str(scale_filename)
        msg_str += status_str
        if print_output: print(status_str)
    
    return (error_in_file, msg_str, scales_lst)



def get_scales_list_from_file(input_sclf, print_output=True):
    '''
    process scales txt file and return a list of list, each list is a scale.
    single element out list structure is:
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
        ]
    scale file must have a strict structure: each scale must have 10 elements (see example file):
        NAME, FOLDER, FILENAME, STRING01, STRING02, STRING03, STRING04, STRING05, STRING06, FOOTER, ARROWS
    this function checks if all elements are present for each scale in correct order
    
    return tuple of parameters: (
      scales_lst
    , msg_str
    )
    
    ie: 
    (
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
            ]
            , [
            ...
            ]
        ]
        , 'Getting Scales from File ...'
    )
    '''
    msg_str = ''
    # scales_lst = [{scale1dict}, {scale2dict}, ..]
    # scalexdict = {'scale_name':'Am Blue..', ..., 'string01':['5,x,x,8',...]...,  }    
    error_in_file, parse_msg, scales_lst = parse_scales_from_file(
          input_sclf
        , print_output=print_output
        )
    msg_str += parse_msg + '\n'
    
    if not error_in_file:
        scl_list, get_scales_msg = get_scales_list(scales_lst, print_output=print_output)
        msg_str += get_scales_msg
    else:
        scl_list = []
    
    return (scl_list, msg_str)



if __name__ == "__main__":
    
    # testing this function
    
    input_sclf = '../tests/scls_tests_files/scale-list.txt'
    print_output = True
    
    scl_list, msg_str = get_scales_list_from_file(input_sclf, print_output=print_output)
    
    print('\nSCALES FROM get_scales_list_from_file')
    
    for scl in scl_list:
        print('*************************************')
        print('error_in_scale:', scl[0])
        print('error_message:', scl[1])
        print('scale_name:', scl[2])
        print('scale_filename:', scl[3])
        print('subfolder:', scl[4])
        for elem1, elem2, elem3 in zip(scl[5], scl[6], scl[7]): 
            print(elem1, '\t', elem2, '\t', elem3)
        print('footer:', scl[8])
        print('arrows:', scl[9])

    print(msg_str)
    