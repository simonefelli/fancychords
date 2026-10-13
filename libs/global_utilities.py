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
global_utilities: small helpers shared by fancychords and fancyscales.

Main groups of functions:
    - strings:     sanitize_str (safe file names), lower_and_underscore, ...
    - chord lists: crd_str2slst ('x,3,2' -> ['x','3','2']), crd_slst2ilst
                   (['x','3'] -> [None, 3]), max_min_fret_slst, ...
    - config:      fill_jdump (complete a json config), param_check
                   (cli > json config > default precedence)
"""

# standard library imports
import json


# Fonts.
# The default font is Ubuntu Mono 0.80 (from ubuntu-font-family-0.83),
# renamed 'Ubuntu Mono derivative FChords' as the Ubuntu Font Licence asks
# for modified fonts: it never mixes with the newer Ubuntu Mono of recent
# systems (bolder, larger) and works the same on Linux and Windows. The font
# files are in the fonts/ folder of the repository.
DEFAULT_FONT_FAMILY = 'Ubuntu Mono derivative FChords'
# fonts accepted by --font-family; 'Ubuntu Mono Legacy' is the name used by
# chords made with older versions (a locally renamed copy of the same font)
FONT_FAMILIES = [DEFAULT_FONT_FAMILY, 'Ubuntu Mono Legacy', 'Ubuntu Mono',
                 'Liberation Mono', 'DejaVu Sans Mono', 'Courier New']


def lower_and_underscore(instr):
    '''
    given an input string this function replace spaces with underscores
    and change all the string to lowercase
    
    ie: lower_and_underscore('Am Blues Scale') 
            -> 'this is old but very aa'
    
    instr: String, input string
    
    return: String, processed string
    '''
    return instr.replace(' ', '_').lower()


def sanitize_str(instr):
    '''
    given an input string this function remove dangerous chars for a filename
    and return the sanitized string, also trucate it if too long.
    Note: original instr is untouched as string is an immutable type variable
    so python will not change it when it is passed
    
    ie: sanitize_str('this is old, but\nvery; "aa"') 
            -> 'this is old but very aa'
    
    instr: String, input string
    
    return: String, sanitized string
    '''
    if instr:
        max_chars = 100
        repl_char = ''
        repl_char_for_newline = ' '
        forb_chars = [
              "'", '\n', ',', '’'
            , ';' , ':', '\\', '/', '"'
            , '?', '[', ']', '=', '^'
            , '<', '>', '&', '$', '£'
            , '*', '(', ')', '!'
            , '|', '~', '`', '´'
            , '{', '}', '%'
            ]
        # safe encoding for windows: keep only plain ascii chars.
        # encode('latin1', 'ignore') drops chars that are not latin1 (ie '♯'),
        # then decode('utf8', 'ignore') drops the remaining non ascii bytes
        # (ie 'è'), so 'DOè♯' -> 'DO'
        instr = instr.encode('latin1', 'ignore').decode('utf8', 'ignore')
        for char in forb_chars:
            if char == '\n':
                instr = instr.replace(char, repl_char_for_newline)
            else:
                instr = instr.replace(char, repl_char)
        # very long names are cut, as some file systems limit name length
        if len(instr) > max_chars: instr = instr[:max_chars]
    return instr


def mytuplechange(mytuple, myindex, myvalue):
    '''
    given a tuple (mytuple) return a new tuple with an element changed.
    This is a workaround cause tupèles are immutable
    
    ie: mytuplechange(('cc', 345, 'tresdf'), 1 , 'xxx') -> ('cc', 'xxx', 'tresdf')
    
    mytuple: Tuple, input tuple to be changed
    myindex: Integer, index of tuple element to be changed
    myvalue: String or Number, nre value of myindex elemnt
    
    return: Tuple, changed tuple
    '''
    
    return tuple(myvalue if idx==myindex else elem for idx, elem in enumerate(mytuple))


def fill_format_fonts(fretx_format, font_weight, font_family):
    """
    return a copy of a fretx_format dict where every format tuple without
    dot_labelfont_weight (index 9) or dot_labelfont_family (index 10)
    gets the global font_weight / font_family.
    
    A copy is returned (instead of changing fretx_format in place) because
    the dict received may be shared, ie it may be the default dict defined in
    fancychords.py: changing it would leak values into the following chords.
    All the keys are processed, so a format like 'b3' or 'rh' coming from the
    json config file gets the global fonts too, and a dict without 'r' is fine.
    
    ie: fill_format_fonts({'*': (1.0, ..., '', '', False, False)}, 'bold', 'Ubuntu Mono')
            -> {'*': (1.0, ..., 'bold', 'Ubuntu Mono', False, False)}
    
    fretx_format: Dict, {interval: format tuple}, see draw_chord() docs
    font_weight: String, global font weight
    font_family: String, global font family
    
    return: Dict, new fretx_format dict
    """
    new_format = {}
    for interval, fmt in fretx_format.items():
        # json config files give lists, not tuples: mytuplechange()
        # handles both and always returns a tuple
        if not fmt[9]: fmt = mytuplechange(fmt, 9, font_weight)
        if not fmt[10]: fmt = mytuplechange(fmt, 10, font_family)
        new_format[interval] = fmt
    return new_format


def fix_duplicate_filenames(items, name_index):
    '''
    make every output file name unique, in place. Used for chords
    (chord_parser) and scales (scale_parser).
    items is a list of lists and items[i][name_index] is a file name
    (without extension). The first item keeps its name, the following
    ones with the same name get a '.vXX' postfix (starting from .v02):
        Cm, Cm, Cm -> Cm, Cm.v02, Cm.v03
    - names are compared ignoring upper/lower case, because on Windows and
      macOS 'Cm7.svg' and 'CM7.svg' are the same file and one image would
      silently overwrite the other
    - a generated name is never one already used by another item, ie:
      Cm, Cm.v02 (given by the user), Cm -> Cm, Cm.v02, Cm.v03
    
    items: List of lists
    name_index: Integer, index of the file name in every inner list
    
    return: items (same list, modified in place)
    '''
    # set of all filenames already taken, compared in lower case (casefold).
    # It is filled with every name given in input, so that a generated
    # '.vXX' name can never clash with a name chosen by the user
    used_names = {item[name_index].casefold() for item in items}
    # set of names already assigned to an item while scanning the list
    assigned_names = set()
    for item in items:
        filename = item[name_index]
        # first time we meet this name: the item keeps it
        if filename.casefold() not in assigned_names:
            assigned_names.add(filename.casefold())
            continue
        # name already assigned to a previous item: look for the first
        # free version number, starting from 2 (the original is version 1)
        vers = 2
        while (filename + '.v' + str(vers).zfill(2)).casefold() in used_names:
            vers += 1
        new_filename = filename + '.v' + str(vers).zfill(2)
        # modify original items and remember the new name as taken
        item[name_index] = new_filename
        used_names.add(new_filename.casefold())
        assigned_names.add(new_filename.casefold())
    return items


def chain(my_elem, prefix = '', postfix = '', nullvalue = ''):
    '''
    format an element for chaining into a string
    
    ie: chain(['T', 'x', None, 2, '1', '3'], '', , ') -> T, x, , 2, 1, 3
    
    my_elem: String, single element
    prefix: String element prefix
    postfix: String element postfix
    nullvalue: Variant, value if null
    
    return: String
    '''
    if my_elem:
        return prefix + my_elem + postfix
    else:
        return nullvalue


def lst2str(mylist, separator, nullvalue):
    '''
    turn list into a string using separator and nullvalue.
    
    ie: lst2str(['T', 'x', None, 2, '1', '3'], ', ', '') -> T, x, , 2, 1, 3
    ie: lst2str(['T', 'x', None, 2, '1', '3'], ', ', 'x') -> T, x, x, 2, 1, 3
    
    mylist: String, single frets/finger string
    separator: String separator
    nullvalue: Variant, value if null
    
    return: String
    '''
    out_list = [str(elem) if elem else nullvalue for elem in mylist]
    return separator.join(out_list)


def crd_str2slst(crd_str):
    '''
    given a single frets/finger string return a splitted frets/finger string list.
    ie: crd_str2lst('T,x, x,2,1 ,3 ') -> ['T', 'x', 'x', '2', '1', '3']
    
    crd_str: String, single frets/finger string
    
    return: List, splitted frets/finger string list
    '''
    # split frets/finger string in a list
    crd_strlist = crd_str.split(',')
    # remove whitespaces from every single frets/finger char
    crd_strlist = [crd.strip() for crd in crd_strlist]
    return crd_strlist


def crd_slst2ilst(crd_slst):
    '''
    given a string frets/finger list return a int frets/finger list.
    if a frets/finger is omitted ('x') return None 
    for that frets/finger (also for finger thumb 'T')
    ie: crd_slst2ilst([' x','0','5','5 ','4','3']) -> [None, 0, 5, 5, 4, 3]
    
    crd_slst: List, frets/finger string list of a chord
    
    return: List, frets/finger int list of a chord
    '''
    # output list
    cint = []
    for cstr in crd_slst:
        # strip extra spaces
        cstr = cstr.strip()
        if cstr.isdigit():
            cint.append(int(cstr))
        else:
            cint.append(None)
    return cint


def crd_ilst2slst(crd_ilst):
    '''
    given a int frets/finger list return a string frets/finger list.
    if a frets/finger is omitted (None) return ('x') 
    ie: crd_ilst2slst([None, 3, 2, 0, 1, 0]) -> ['x', '3', '2', '0', '1', '0']
    
    crd_ilst: List, frets/finger int list of a chord
    
    return: List, frets/finger string list of a chord
    '''
    # output list
    cstr = []
    for cint in crd_ilst:
        if (cint is not None):
            cstr.append(str(cint))
        else:
            cstr.append('x')
    return cstr


def list_filter(list_int, omit_zeros):
    '''
    given an input list on integers and None elements, return
    original list filtered from None if omit_zeros is False
    or original list filtered from Nones and zeros if omit_zeros is true.
    For example:
        list_filter([None, 0, 6, 5, 6, 4], False) -> [0, 6, 5, 6, 4]
        list_filter([None, 0, 6, 5, 6, 4], True) ->     [6, 5, 6, 4]
    
    list_int: List, input list of positive integers, there can be Nones and zeros
    omit_zeros: Boolean, if True filter out Nones and zeros
                if false filter out Nones only
    
    return: List, original list filtered (see above)
    '''
    # use of list() function to make source more py3onic 
    if omit_zeros:
        lst_flt = list([elem for elem in list_int if elem])
    else:
        lst_flt = list([elem for elem in list_int if (elem is not None)])
    return lst_flt
    

def frets_int_normalize(frets_int):
    '''
    check if chord form is movable (is_movable_form) and
    return if chord form is movable, normalized chord to fret 1 and
    half-steps of offset used to normalize
    chord form, ie: [None, 4, 6, 5, 6, 4] -> (True,  [None, 1, 3, 2, 3, 1], 3)
                    [None, 3, 2, 0, 1, 0] -> (False, [None, 3, 2, 0, 1, 0], 0)
                    
    frets_int: List, numbers fret list of a chord
    
    return:
    - is_movable_form: Boolean, True if chord form is movable
    - frets_int_norm: List, fret list normalized
    - offset half-steps used to normalize
    '''
    is_movable_form = False
    # keep only numbers from frets_int (filter None)
    # frets_int = [None, 4, 6, 5, 6, 4] -> frets_int_flt = [4, 6, 5, 6, 4]    
    frets_int_flt = list_filter(frets_int, False)
    # all strings muted (x,x,x,x,x,x): nothing to normalize
    # (min() of an empty list raised ValueError)
    if not frets_int_flt: return (False, list(frets_int), 0)
    # compute min_fret: number, min fret present in chord
    min_fret = min(frets_int_flt)
    # if min_fret is > 0 then chord form is movable
    if min_fret > 0:
        is_movable_form = True
        # we can normalize it
        frets_int_norm = [(fret-min_fret+1) if fret else None for fret in frets_int]
    else:
        # otherwise just return original list
        frets_int_norm = list(frets_int)
    frets_int_norm_flt = list_filter(frets_int_norm, False)
    new_min_fret = min(frets_int_norm_flt)
    delta_frets = min_fret - new_min_fret
    return (is_movable_form, frets_int_norm, delta_frets)


def max_min_fret_slst(frets_slst, omit_zeros=True):
    """
    return max fret number and min fret number where for
    calculating min fret. Zeros are omitted if omit_zeros is True
    (this is the default) while 'x' are always omitted
    note: ['x','x','x','x', ....] -> f() -> (0, 0)

    frets_slst: List of strings, fret sequence

    return a tuple: (max_fret, min_fret)
    """
    # replace non digits chars from fret list with None and convert digits to int: 
    # ['x','0','6','5','6','4'] -> [None, 0, 6, 5, 6, 4]
    frets_int = crd_slst2ilst(frets_slst)
    # ============ compute max_fret and min_fret ============
    # keep only numbers from frets_int (filter None and 0)
    # frets_int = [None, 4, 6, 5, 6, 4] -> frets_int_flt = [4, 6, 5, 6, 4]
    # frets_int = [None, 4, 6, 0, 6, 4] -> frets_int_flt = [4, 6, 6, 4]
    frets_int_flt = list_filter(frets_int, omit_zeros)
    # min fret - > 4
    min_fret = min(frets_int_flt) if frets_int_flt else 0
    # max fret - > 6
    max_fret = max(frets_int_flt) if frets_int_flt else 0

    return (max_fret, min_fret)


def traspose_fretb(fretb_slst):
    """
    Transpose a fretboard matrix in a way like that:
    Guitar neck from fret 5 to 8 (1st list is high e String, 6th is low E String)
    [
          ['5', 'x', 'x', '8']
        , ['5', 'x', 'x', '8']
        , ['5', 'x', '7', '8']
        , ['5', 'x', '7', 'x']
        , ['5', '6', '7', 'x']
        , ['5', 'x', 'x', '8']
    ]
    -> 4 guitar chords
    [
          ['5', '5', '5', '5', '5', '5']
        , ['x', '6', 'x', 'x', 'x', 'x']
        , ['x', '7', '7', '7', 'x', 'x']
        , ['8', 'x', 'x', '8', '8', '8']
    ]
    
    fretb_slst: list of string lists (6 elements, one for every guitar String) 
           every element must have same lenght 
           every element can represent frets positions or intervals positions or dlabels positions
           of a Guitar String
        ie: [['5', 'x', 'x', '8'],  ['5', 'x', 'x', '8'], ...] or
            [['R', 'x', 'x', 'b3'], ['5', 'x', 'x', 'b7'], ...] or 
            [['1', 'x', 'x', '4'],  ['1', 'x', 'x', '4'], ...]
        
    return list of string lists trasposed fretboard matrix
    """
    # compute len_fretb, chcek if fretb_slst exist also 
    len_fretb = len(fretb_slst[0] if fretb_slst else [])

    # initalise fretb_transp lists to [[], [], [], [] , ...]
    # '_': better coding style, since, the index variable is ignored
    fretb_transp = [[] for _ in range(len_fretb)]
    
    if len_fretb:
        for fretb_elem in fretb_slst:
            for n in range(len_fretb):
                # insert(0, elem) is used to append in a list in reverse order
                # this is because in fretb_slst first list is for higher 1st String
                # while in fretb_transp list each list element is a chord 
                # [E-String, A-String, B-String, ... e-String] and start from bottom 6th String
                fretb_transp[n].insert(0, fretb_elem[n])
    
    return fretb_transp


def max_min_fretb_slst(fretb_slst):
    """
    ** CURRENTLY NOT USED BUT USEFUL FOR FUTURE **
    given a fretb matrix return max fret number and min fret number for the whole matrix.
    Where for calculating min fret, zeros are not omitted but 'x' are

    fretb_slst: list of string lists every element must have same lenght and 
           can represent frets or Strings of a Guitar Neck
        ie: guitar neck Strings meaning (1st list is high e String, 6th is low E String,
            horizantal way)
            [
                  ['5', 'x', 'x', '8']
                , ['5', 'x', 'x', '8']
                , ['5', 'x', '7', '8']
                , ['5', 'x', '7', 'x']
                , ['5', '6', '7', 'x']
                , ['5', 'x', 'x', '8']
            ]
            or chord meaning (vertical way)
            [
                  ['5', '5', '5', '5', '5', '5']
                , ['x', '6', 'x', 'x', 'x', 'x']
                , ['x', '7', '7', '7', 'x', 'x']
                , ['8', 'x', 'x', '8', '8', '8']
            ]
            max_min_fretb_slst will output (5, 8)
            
    Note: for a scale list like that
        [
          ['x','x','x','7','x','x','10','x','x']
        , ['x','x','x','7','8','x','x' ,'x','x']
        , ['x','x','x','7','x','x','x' ,'x','x']
        , ['x','x','x','x','x','9','x' ,'x','x']
        , ['x','x','x','x','x','9','10','x','x']
        , ['x','x','x','7','x','x','10','x','x']
        ]
    max_min_fretb_slst will always output (10, 7) not (12, 4)
    to overcome this see below the max_min_scales_slst function

    return a tuple: (max_fret, min_fret)
    """
    
    # strip empty spaces in strgs_frets_list
    fretb_slst_strip = [[elem.strip() for elem in frets] for frets in fretb_slst]
    
    # filter all rows like ['x','x','x','x', ...]
    # otherwise using max_min_fret_slst() below you get 0 and this count as a min=0
    frets_fltrd = [frets for frets in fretb_slst_strip if not all((elem.lower() == 'x') for elem in frets)]
    
    # use max_min_fret_slst() to get max and min of each 1 fretb_slst element and append results
    # to a list (min_max_list). Note zeros are not omitted in max_min_fret_slst() function.
    # This is a 2 deep List Comprehension because each time max_min_fret_slst()
    # return value is a tuple. The effect is: [f([List1]), f([List2]), ..] -> [(A, B), (C, D), ..] -> [ A, B, C, D, ..]
    min_max_list = [min_max for frets in frets_fltrd for min_max in max_min_fret_slst(frets, omit_zeros=False)]
    max_fret = max(min_max_list) if min_max_list else 0
    min_fret = min(min_max_list) if min_max_list else 0
    
    return max_fret, min_fret


def max_min_scales_slst(strgs_frets_list):
    """
    given a scale matrix return max fret number and min fret number for the whole matrix.
    Where for calculating min fret, zeros are not omitted and also 'x' are 
    taken into account

    strgs_frets_list: list of string lists every element must have same lenght and 
           represent a String of a Guitar Neck: 1st list is high e String, 
           6th is low E String (horizantal way)
           example1
            [
                  ['7','x','x','10']
                , ['7','8','x','x' ]
                , ['7','x','x','x' ]
                , ['x','x','9','x' ]
                , ['x','x','9','10']
                , ['7','x','x','10']
            ]
           example2
            [
                  ['x','x','x','7','x','x','10','x','x']
                , ['x','x','x','7','8','x','x' ,'x','x']
                , ['x','x','x','7','x','x','x' ,'x','x']
                , ['x','x','x','x','x','9','x' ,'x','x']
                , ['x','x','x','x','x','9','10','x','x']
                , ['x','x','x','7','x','x','10','x','x']
            ]
    for example1 max_min_scales_slst will return (10, 7)
    for example2 max_min_scales_slst will return (12, 4) as 'x' are
    taken into account

    return a tuple: (max_fret, min_fret)
    """
    
    # strip empty spaces in strgs_frets_list
    strgs_frets_list_strip = [[elem.strip() for elem in frets] for frets in strgs_frets_list]
    
    # filter all rows like ['x','x','x','x', ...]
    # otherwise you get 0 and this count as a min=0
    strgs_frets_fltrd = [frets for frets in strgs_frets_list_strip if not all((elem.lower() == 'x') for elem in frets)]
    
    if strgs_frets_fltrd:
        
        min_list = []
        max_list = []
    
        for row in strgs_frets_fltrd:
            
            # for every row find first numerical min and if there are previous 'x'
            # then count back (subtract to the found min). 
            # Append all mins to a list (min_list)
            found_flag = False
            min_row = 0
            for index, elem in enumerate(row):
                if found_flag: break
                if elem.isdigit():
                    last_number = int(elem)
                    min_row = last_number - index
                    found_flag = True
            min_list.append(min_row)
            
            # make a copy of row and reverse it, otherwise
            # with xx.rerverse() you reverse the original row list
            # then for every row find first numerical max and if there are previous 'x'
            # then add them to that max. Append all maxs to a list (max_list)            
            row_reverse = row[::-1]
            found_flag = False
            max_row = 0
            for index, elem in enumerate(row_reverse):
                if found_flag: break
                if elem.isdigit():
                    last_number = int(elem)
                    max_row = last_number + index
                    found_flag = True
            max_list.append(max_row)
            
            final_max, final_min = max(max_list), min(min_list)

    else:
        
        final_max, final_min = None, None
        
    return final_max, final_min


def fill_jdump(db_dict_jdump, fd_k, radius_k, barre_k):
    '''
    This function take the json config file db_dict_jdump and check
    if there are missing parameters that can be calculated from others
    with known formulas.
    If so db_dict_jdump is modified in place with missing parameters added
    
    db_dict_jdump: Dict, dict from json config file
    fd_k: Number, multiply factor to calculate fd, None to disable
    radius_k: Number, multiply factor to calculate radius_factor, None to disable
    barre_k: Number, multiply factor to calculate barre_strk_wdth, None to disable
    
    return: None
    '''
    
    # if parameters section is in json config file
    if db_dict_jdump.get('parameters'):
        
        # these parameters must exist
        sd = db_dict_jdump['parameters'].get('sd')
        lntk = db_dict_jdump['parameters'].get('lntk')
        
        # otherwise end function here
        if (not sd) or (not lntk): return
        
        # if sd and lntk exist these other parameters can be calculated    
        fd = db_dict_jdump['parameters'].get('fd')
        radius_factor = db_dict_jdump['parameters'].get('radius_factor')
        barre_strk_wdth = db_dict_jdump['parameters'].get('barre_strk_wdth')
        
        # if fd is missing then calculate it and add it to dict
        if not fd and fd_k:
            db_dict_jdump['parameters']['fd'] = sd * fd_k
            # print(db_dict_jdump['parameters']['fd'])
        
        # if radius_factor is missing then calculate it and add it to dict
        if not radius_factor and radius_k:
            db_dict_jdump['parameters']['radius_factor'] = radius_k / sd
            # print(db_dict_jdump['parameters']['radius_factor'])
        
        # if barre_strk_wdth is missing then calculate it and add it to dict
        if not barre_strk_wdth and barre_k:
            db_dict_jdump['parameters']['barre_strk_wdth'] = barre_k * lntk
            # print(db_dict_jdump['parameters']['barre_strk_wdth'])
    
    return


def overload_config_json(json_file_path, chords_scale_flag='chords', **overload_params):
    '''
    Given an input json config file this function return 2 tuple of params from json file. 
    All these params can be overloaded by **overload_params keyword arguments.
    First out tuple is in the format accepted by process_chords or process_scales_file functions.
    chords_scale_flag set this function to work with chords or scales
    
    Second out tuple are params accepted by generate_htmlreport function.
    
    json_file_path: String, json file path
    
    chords_scale_flag: String, can be 'chords' or 'scales', default is chords
    
    **overload_params: keyword arguments, sequence of params and their value 
    (similar to a dict) ie: dir_output = './dirout/chords', report = 'enable'
    
    return Tuple of tuples: 
        (
          process_params
        , report_params
        )
    Both 2 tuple of config params can be overloaded by **overload_params
    '''
    
    # dict with all params from json file
    args = {}
    
    # handle json config file
    # note: unlike fancychords.py / fancyscales.py there are no defaults
    # here, so the json file must be complete (all 4 sections and all the
    # params), like tests/json_cfg_tests_files/default_chords_config.json.
    # Keyword arguments with a name that is not a known param are ignored
    with open(json_file_path, 'r', encoding='utf-8') as jsonfile: db_dict_jdump = json.load(jsonfile)
    
    # get all subsections dicts
    io_dict = db_dict_jdump['i/o']
    flags_dict = db_dict_jdump['flags']
    format_dict = db_dict_jdump['generic_formats']
    parameters_dict = db_dict_jdump['parameters']
    
    # Get all params from json file, dict.get(myparam) return None if 
    # myparam do not exist
    
    # -- parameters --
    args['lntk'] = parameters_dict.get('lntk')
    args['x_or'] = parameters_dict.get('x_or')
    args['y_or'] = parameters_dict.get('y_or')
    args['ns'] = parameters_dict.get('ns')
    args['nf'] = parameters_dict.get('nf')
    args['fd'] = parameters_dict.get('fd')
    args['sd'] = parameters_dict.get('sd')
    args['radius_factor'] = parameters_dict.get('radius_factor')
    args['ncols'] = parameters_dict.get('ncols')
    args['thumb_width'] = parameters_dict.get('thumb_width')
    if chords_scale_flag == 'chords':
        args['barre_strk_wdth'] = parameters_dict.get('barre_strk_wdth')
    elif chords_scale_flag == 'scales':
        args['padding'] = parameters_dict.get('padding')
   
    # -- directory out --
    args['dir_output'] = io_dict.get('dir_output')
    
    # -- flags --
    args['horiz'] = flags_dict.get('horiz')
    args['enable_header'] = flags_dict.get('enable_header')
    args['enable_dotlabels'] = flags_dict.get('enable_dotlabels')
    args['enable_footer'] = flags_dict.get('enable_footer')
    args['enable_fretnum'] = flags_dict.get('enable_fretnum')
    args['nutline'] = flags_dict.get('nutline')
    args['fret0'] = flags_dict.get('fret0')
    args['convert_flag'] = flags_dict.get('convert_flag')
    args['report'] = flags_dict.get('report')
    args['debug'] = flags_dict.get('debug')
    # args['root_is_different'] = flags_dict.get('root_is_different')
    if chords_scale_flag == 'chords':
        args['chord_label_isbottom'] = flags_dict.get('chord_label_isbottom')
        args['chord_label_isleft'] = flags_dict.get('chord_label_isleft')
        args['enable_barre'] = flags_dict.get('enable_barre')        
    elif chords_scale_flag == 'scales':
        args['scale_label_isbottom'] = flags_dict.get('scale_label_isbottom')
        args['scale_label_isleft'] = flags_dict.get('scale_label_isleft')
    
    # -- generic_formats --
    args['font_weight'] = format_dict.get('font_weight')
    args['font_family'] = format_dict.get('font_family')
    args['upper_labels_font_weight'] = format_dict.get('upper_labels_font_weight')
    args['upper_labels_font_family'] = format_dict.get('upper_labels_font_family')
    args['upper_labels_font_factor'] = format_dict.get('upper_labels_font_factor')
    args['bottom_labels_font_weight'] = format_dict.get('bottom_labels_font_weight')
    args['bottom_labels_font_family'] = format_dict.get('bottom_labels_font_family')
    args['bottom_labels_font_factor'] = format_dict.get('bottom_labels_font_factor')
    args['side_labels_font_weight'] = format_dict.get('side_labels_font_weight')
    args['side_labels_font_family'] = format_dict.get('side_labels_font_family')
    args['side_labels_font_factor'] = format_dict.get('side_labels_font_factor')
    args['fretb_format'] = format_dict.get('fretb_format')
    args['fret0_format'] = format_dict.get('fret0_format')
    if chords_scale_flag == 'chords':
        args['chord_label_font_weight'] = format_dict.get('chord_label_font_weight')
        args['chord_label_font_family'] = format_dict.get('chord_label_font_family')
        args['chord_label_font_factor'] = format_dict.get('chord_label_font_factor')    
    elif chords_scale_flag == 'scales':
        args['scale_label_font_weight'] = format_dict.get('scale_label_font_weight')
        args['scale_label_font_family'] = format_dict.get('scale_label_font_family')
        args['scale_label_font_factor'] = format_dict.get('scale_label_font_factor')
        args['arrows_format'] = format_dict.get('arrows_format')


    # perform params overloading (param_name in args -> get the keys)
    for param_name, param_value in overload_params.items():
        if param_name in args: args[param_name] = param_value
    
    # pack some params together in a tuple sequence accepted by process_chords/process_scales_file functions
    process_params = None
    if chords_scale_flag == 'chords':
        process_params = (
                args['dir_output'], args['horiz'], args['enable_header'], args['enable_dotlabels'], 
                args['enable_footer'], args['enable_barre'], args['enable_fretnum'], 
                args['barre_strk_wdth'], args['nutline'], args['fret0'], 
                args['font_weight'], args['font_family'],
                args['chord_label_font_weight'], args['chord_label_font_family'], 
                args['chord_label_font_factor'], args['chord_label_isbottom'], args['chord_label_isleft'],
                args['fretb_format'], args['fret0_format'], 
                args['upper_labels_font_weight'], args['upper_labels_font_family'], args['upper_labels_font_factor'], 
                args['bottom_labels_font_weight'], args['bottom_labels_font_family'], args['bottom_labels_font_factor'], 
                args['side_labels_font_weight'], args['side_labels_font_family'], args['side_labels_font_factor'],
                args['lntk'], args['x_or'], args['y_or'], args['ns'], args['nf'], args['fd'], args['sd'], args['radius_factor'],
                args['convert_flag'], args['debug']
                )
    elif chords_scale_flag == 'scales':
        process_params = (
                args['dir_output'], args['horiz'], args['enable_header'], args['enable_dotlabels'], 
                args['enable_footer'], args['enable_fretnum'], args['nutline'], 
                args['fret0'], args['font_weight'], args['font_family'],
                args['scale_label_font_weight'], args['scale_label_font_family'], 
                args['scale_label_font_factor'], args['scale_label_isbottom'], args['scale_label_isleft'],
                args['fretb_format'], args['fret0_format'], args['arrows_format'], args['padding'], 
                args['upper_labels_font_weight'], args['upper_labels_font_family'], args['upper_labels_font_factor'], 
                args['bottom_labels_font_weight'], args['bottom_labels_font_family'], args['bottom_labels_font_factor'], 
                args['side_labels_font_weight'], args['side_labels_font_family'], args['side_labels_font_factor'],
                args['lntk'], args['x_or'], args['y_or'], args['ns'], args['nf'], args['fd'], args['sd'], args['radius_factor'],
                args['convert_flag'], args['debug']
                )
    
    # pack some params together in a tuple sequence accepted by generate_htmlreport function
    report_params = (
        args['report'],
        args['dir_output'],
        args['ncols'],
        args['thumb_width']
    )

    return process_params, report_params


def param_check(db_dict_jdump, args_param, param_name, param_section, default_params):
    '''
    This function is used to check if a parameter of fancychord is set by cli,
    by config file or is just as default. This logic applies: 
    cli has highest precedence, then comes json config file and at last default. 
    So if, say, MyPar is set 'A' from cli, 'B' from config file and is 'C' by default
    then 'A' wins. param_check return a tuple with actual param value 
    (set by precedence logic) and a boolean which tell us if param is as default or not
    
    db_dict_jdump: Dict, dict from json config file
    args_param: parser argument value (None as default if not set)
    param_name: String, parameter name
    param_section: String, parameter section of config json file
    default_params: default params dict
    
    ie: param_check(
            db_dict_jdump, args.dir_output, 
            'dir_output', 'i/o', 
            default_params) -> ('./', True)
    
    return: Tuple
        - param value (type varies) set by precedence logic
        - boolean, param is as default or not
    '''
    
    default_value = default_params[param_name]
    # make a copy of default_params to avoid losing default data (by reference issue)
    final_params = dict(default_params)
    
    # if a json config file is provided
    if db_dict_jdump:
        # get section (None if it is not present in json file)
        j_sect = db_dict_jdump.get(param_section)
        # get param (None if section or param are not present in json file).
        # note: j_param must always be defined here, even when the section
        # exists but is empty (ie: "flags": {}), otherwise the check below
        # would raise an UnboundLocalError
        j_param = j_sect.get(param_name) if j_sect else None
        # a param explicitly set to null in json file counts as "not set"
        # so the default value is kept
        if j_param is not None:
            # copy the value in final_params dict
            final_params[param_name] = j_param

    # if parm is set by cli
    if args_param is not None:
        # copy the value in final_params dict
        final_params[param_name] = args_param
    
    # if parm value is like default
    if final_params[param_name] == default_value:
        # set boolean variable to True
        same_as_default = True
    else:
        same_as_default = False
    
    return (final_params[param_name], same_as_default)



if __name__ == "__main__":
   
    # testing this functions
    
    print('- lower_and_underscore(\'Am Blues Scale\'): '+ lower_and_underscore('Am Blues Scale'))

    instr = 'this is o/ld, but\nver\\y l’it}t£e; "aa"'
    print('\n- sanitize_str():\n\toriginal string:\n\t----------------')
    print('\t' + instr)
    outstr = sanitize_str(instr)
    print('\t----------------\n\tchanged string:\n\t----------------')
    print('\t' + outstr)
    print('\t----------------')

    print('\n- chain(\'apple\', \'/\', \'_\', None\'):\n\t', chain('apple', '/', '_', None))


    test_list1, myseparator, mynullvalue = ['T', 'x', None, 2, '1', '3'], ', ', ''
    print('\n- lst2str(' + str(test_list1) + ', \'' + myseparator + '\', \'\'):\n\t', lst2str(test_list1, myseparator, mynullvalue))
    
    test_chords = (
          [' 5','4','0','0','5 ','5']
        , [' x','3','5','5 ','4','3']
        , ['x','1','3','1','2','1']
        , ['x','4','6','5','6','4']
        , ['x','3','2','0','1','0']
        )
    for chord_slist in test_chords:
        chord_ilist = crd_slst2ilst(chord_slist)
        print('\n- crd_slst2ilst(' + str(chord_slist) + '):\n\t', chord_ilist)
        print('\n- crd_ilst2slst(' + str(chord_ilist) + '):\n\t', crd_ilst2slst(chord_ilist))

    test_chord1 = ' T, x,x,2 ,1,3 '
    print('\n- crd_str2slst(' + str(test_chord1) + '):\n\t', crd_str2slst(test_chord1))
    
    print('\n- list_filter([None, 3, 2, 0, 1, 0], False):\n\t', list_filter([None, 3, 2, 0, 1, 0], False))
    print('\n- frets_int_normalize([None, 7, 6, 4, 5, 4]):\n\t', frets_int_normalize([None, 7, 6, 4, 5, 4]))
    print('\n- max_min_fret_slst(["x","0","6","5","6","4"]):\n\t', max_min_fret_slst(['x','0','6','5','6','4']))



    fretb = [
          ['5', 'x', 'x', 'x']
        , ['5', 'x', 'x', 'x']
        , ['5', 'x', '7', 'x']
        , ['5', 'x', '7', 'x']
        , ['5', '6', '7', 'x']
        , ['5', 'x', 'x', 'x']
        ]
    
    '''
    
    # fretb = [[], [], [], []]
    fretb = []
    
    '''
    
    fretb_transp = traspose_fretb(fretb)
    print('\n- traspose_fretb(')
    for elem in fretb: print('\t', elem)
    print('\t) ---> fretb_transp = ')
    if fretb_transp:
        for elem in fretb_transp:
            print('\t', elem)
    else:
        print(fretb_transp)
    print('\n- max_min_fretb_slst(fretb_transp): ', max_min_fretb_slst(fretb_transp))
    
    fretb_allneck1 = [
              ['x','x','2','3','x','x','x','7','x','x','10','x' ,'x' ,'x','14','15','x' ]
            , ['x','x','x','3','x','x','x','7','8','x','x' ,'x' ,'12','x','x' ,'15','x' ]
            , ['0','x','x','x','4','x','x','7','x','x','x' ,'11','12','x','x' ,'x' ,'16']
            , ['0','x','x','x','4','5','x','x','x','9','x' ,'x' ,'12','x','x' ,'x' ,'16']
            , ['x','x','2','x','x','5','x','x','x','9','10','x' ,'x' ,'x','14','x' ,'x' ]
            , ['x','x','2','3','x','x','x','7','x','x','10','x' ,'x' ,'x','14','15','x' ]
        ]
    print('\n- max_min_fretb_slst(')
    for elem in fretb_allneck1: print('\t', elem)
    print('\t): ->', max_min_fretb_slst(fretb_allneck1))

    fretb_allneck2 = [
              ['x','x','x','x','x','x','x','7','x','x','10','x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','7','8','x','x' ,'x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','7','x','x','x' ,'x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','x','x','9','x' ,'x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','x','x','9','10','x','x','x','x','x','x']
            , ['x','x','x','x','x','x','x','7','x','x','10','x','x','x','x','x','x']
        ]
    print('\n- max_min_scales_slst(')
    for elem in fretb_allneck2: print('\t', elem)
    print('\t): ->', max_min_scales_slst(fretb_allneck2))
    
    
    print('\n- overload_config_json')
    print(
        overload_config_json(
        '../tests/json_cfg_tests_files/config_caged_chords.json'
        , 'chords'
        , barre_strk_wdth = 3.8
        , thumb_width = '500.0px'
        )
    )