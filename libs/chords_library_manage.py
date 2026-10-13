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
chords_library_manage: checks for big chord list files (chord libraries).

    check_duplicate_rows_infile    same name, frets and fingers more times
    check_duplicate_chords_infile  same frets with different names
                                   (ie Bm11 and Dsus2/B)
    check_movable_chords_infile    group chords by shape (movable shapes
                                   are compared after moving them to fret 1)

All of them print their report and use chord_parser to read the file, so
chords with syntax errors are skipped.
"""


# local application imports
from libs import global_utilities
from libs import music_utilities
from libs import chord_parser


def check_duplicate_rows_infile(input_crdf):
    '''
    given a chord list txt file print duplicate chords rows in it. Rows are equal 
    if chord_name AND frets AND fingers are equals
    
    input_crdf: String, chord list txt file path. Text file is like:
        NAME     FRETS         FINGERS       LABELS   FOOTER   SUBFOLDER
        Aadd9    x,0,2,4,2,0   x,x,1,4,2,x   %        %        A/Add
    
    return: Text output
        Duplicate Rows:
        dm9   | Chords n.:  [348, 405]
    note: the numbers are positions among the chords loaded from the file
    (1 = first chord), not line numbers of the file: header, comments,
    empty lines and chords with errors are not counted
    '''
    # get_crd_list_from_file -> (crd_list, msg_str)
    # where crd_list is    
    # [
    #    [chord_name, root_note, chord_filename, 
    #    frets, fingers, dlabels, footer, 
    #    subfolder, chord_quality, chord_detail, chord_slash]
    #    , ...
    # ]
    crd_list_from_file = chord_parser.get_crd_list_from_file(input_crdf, print_output=False)
    # crd_chk_list = [(chord_name_lowercase, frets_lowercase, fingers_lowercase), ...]
    # for every elem in crd_chk_list, change all lists in tuples for hashing in finding elemets in dict
    # crd_chk_list = [('dm9', ('x','5','3','5','5','0'),  ('x','2','1','3','4','x')), ...]
    crd_chk_list =[]
    for elem in crd_list_from_file[0]:
        chord_name = elem[0].lower()
        frets = tuple(map(str.lower, elem[3]))
        fingers = tuple(map(str.lower, elem[4]))
        crd_chk_list.append((chord_name, frets, fingers))

    print('\nDuplicate Rows:' + '\n---------------')
    # chords_dupes_dict, dictionary with key =  crd_chk_list single element
    # and value is a list of positions in which key is found in crd_chk_list
    # {('aadd9/mi', ('0','7','7','6','0','0'), ('x','2','3','1','x','x')): [4,54,32], ... }
    chords_dupes_dict = {}
    for chord_index, chord in enumerate(crd_chk_list):
        if chord not in chords_dupes_dict.keys():
            chords_dupes_dict[chord] = [chord_index+1]
        else:
            chords_dupes_dict[chord].append(chord_index+1)
    # duplicate rows are chords with list of positions longer than 1 element
    for key, val in chords_dupes_dict.items():
        if len(val) > 1:
            print(key[0] + '\t | Chords n.: ', val)


def check_duplicate_chords_infile(input_crdf):
    '''
    given a chord list txt file print duplicate chords found in it. Chords are equal 
    if frets only are equals.
    
    input_crdf: String, chord list txt file path. Text file is like:
        NAME     FRETS         FINGERS       LABELS   FOOTER   SUBFOLDER
        Aadd9    x,0,2,4,2,0   x,x,1,4,2,x   %        %        A/Add
    
    return: Text output
        Duplicate Chords:
        * ('x', '2', '0', '2', '3', '0') --> [['Bm11', 'Dsus2/B'], [['x', '1', 'x', '2', '3', 'x']]]
        * ('2', '2', '4', '4', '2', '2') --> [['Bsus2', 'F#sus4'], [['1', '1', '3', '4', '1', '1']]]
    '''
    # get_crd_list_from_file -> (crd_list, msg_str)
    # where crd_list is    
    # [
    #    [chord_name, root_note, chord_filename, 
    #    frets, fingers, dlabels, footer, 
    #    subfolder, chord_quality, chord_detail, chord_slash]
    #    , ...
    # ]
    
    # [
    #     ['G#dim7(no5)/F#', 'G#', ''G#dim7(no5)_F#', 
    #     ['2', '2', '0', '1', '0', '1'], ['3', '4', 'x', '1', 'x', '2'], ['b7', 'b3', 'b5', 'R', 'b3', 'bb7'], 
    #     ['b7', 'b3', 'b5', 'R', 'b3', 'bb7'], ['3', '4', 'x', '1', 'x', '2'],
    #     'Diminished/', 'dim7','(no5)', 'F#']
    #     , ...
    # ]
    crd_list_from_file = chord_parser.get_crd_list_from_file(input_crdf, print_output=False)
    # out_dict = {
    #      ('x','2','4','2','2','4'): [['B13sus2', 'F#sus4', ...], [['x','1','3','1','1','4'], ...]]
    #    , ('x','4','6','6','6','4'): [...]
    #    , ...
    #    }
    out_dict = {}
    print('\nDuplicate Chords:' + '\n---------------------')
    for chord in crd_list_from_file[0]:
        # ' Aadd9'
        chord_name = chord[0]
        # turn frets list into a tuple for being hashable as key in a dict
        # ['2','x','0','2','3','2'] -> ('2','x','0','2','3','2')
        frets = tuple(chord[3])
        # ['x','1','3','1','1','4']
        fingers = chord[4]
        # if this chord is already present in out_dict in terms of frets
        if frets in out_dict:
            # if this is a new chord name for that variant
            if chord_name not in out_dict[frets][0]:
                # append new name
                out_dict[frets][0].append(chord_name)
            # if this is a new fingers pattern for that variant
            if fingers not in out_dict[frets][1]:
                # append new fingers pattern
                out_dict[frets][1].append(fingers)
        else:
            # else append whole new variant
            out_dict[frets] = [[chord_name], [fingers]]
    for key, elem in out_dict.items():
        if len(elem[0]) > 1:
            print('*', key, '-->', elem)


def check_movable_chords_infile(input_crdf):
    '''
    given a chord list txt file check if each chord is movable
    using chord_normalize function (music_utilities.chord_normalize())
    
    input_crdf: String, chord list txt file path. Text file is like:
        NAME     FRETS         FINGERS       LABELS   FOOTER   SUBFOLDER
        Aadd9    x,0,2,4,2,0   x,x,1,4,2,x   %        %        A/Add
    
    return: Text output. For each chord we have movable info
                        , normalized frets tuple
                        , list of chord names of the same shape (all traspositions)
                        , list of possible fingering
    ie:
        Movable: 105
        ---------------------
        > ('1','3','1','2','3','1') --> [['A13','G13'],[['1','3','1','2','4','1']]]
        > ('1','3','1','2','1','1') --> [['A7','F#7','G7'],[['1','3','1','2','1','1']]]
        ....
        Not Movable: 231 
        ---------------------
        > ('x','1','2','0','2','x') --> [['A#dim7','Bbdim7'],[['x','1','2','x','3','x']]]
        > ('2','0','0','2','3','2') --> [['D/F#'],[['1','x','x','2','4','3'],['T','x','x','1','3','2']]]
        ....
    '''
    # get_crd_list_from_file -> (crd_list, msg_str)
    # where crd_list is    
    # [
    #    [chord_name, root_note, chord_filename, 
    #    frets, fingers, dlabels, footer, 
    #    subfolder, chord_quality, chord_detail, chord_slash]
    #    , ...
    # ]
    crd_list_from_file = chord_parser.get_crd_list_from_file(input_crdf, print_output=False)
    # out_movable_dict = {
    #      ('x','1','3','1','1','3'): [['B13sus2'], [['x','1','3','1','1','4']]]
    #    , ('x','2','1','2','1','x'): [['C7b9','C#7b9','E7b9'], [['x','2','1','3','1','x'], ['x','3','1','4','2','x']]]
    #    , ...
    #    }
    out_movable_dict = {}
    out_not_movable_dict = {}
    for chord in crd_list_from_file[0]:
        # ' Aadd9'
        chord_name = chord[0]
        #  ['2','x','0','2','3','2']
        frets = chord[3]
        #  ['x','1','3','1','1','4']
        fingers = chord[4]
        # use chord_normalize function for checking if movable
        # chord_normalize(['4','x','2','4','5','4']) -> (True, [3, None, 1, 3, 4, 3], 1)
        is_movable_form, frets_int_norm, _delta_frets = music_utilities.chord_normalize(frets)
        
        # turn frets int list -> frets str list -> frets str tuple
        # [None, 3, 2, 0, 1, 0] -> crd_slst2ilst() -> ['x', '3', '2', '0', '1', '0'] ->
        #  -> tuple() -> ('x', '3', '2', '0', '1', '0')
        # we need a tuple for being hashable as key in a dict
        frets_tpl_norm = tuple(global_utilities.crd_ilst2slst(frets_int_norm))
        if is_movable_form:
            # check keys of out_movable_dict 
            if frets_tpl_norm in out_movable_dict:
                if chord_name not in out_movable_dict[frets_tpl_norm][0]:
                    out_movable_dict[frets_tpl_norm][0].append(chord_name)
                if fingers not in out_movable_dict[frets_tpl_norm][1]:
                    out_movable_dict[frets_tpl_norm][1].append(fingers)
            else:
                out_movable_dict[frets_tpl_norm] = [[chord_name], [fingers]]
        else:
            if frets_tpl_norm in out_not_movable_dict:
                if chord_name not in out_not_movable_dict[frets_tpl_norm][0]:
                    out_not_movable_dict[frets_tpl_norm][0].append(chord_name)
                if fingers not in out_not_movable_dict[frets_tpl_norm][1]:
                    out_not_movable_dict[frets_tpl_norm][1].append(fingers)
            else:
                out_not_movable_dict[frets_tpl_norm] = [[chord_name], [fingers]]  
    
    print('\nMovable: ' + str(len(out_movable_dict)) + '\n---------------------')
    for key, elem in out_movable_dict.items():
        print('>', key, '-->', elem)
    print('\nNot Movable: ' + str(len(out_not_movable_dict)) + '\n---------------------')
    for key, elem in out_not_movable_dict.items():
        print('>', key, '-->', elem)



if __name__ == "__main__":
    
    # testing this functions
    
    print('------------------  testing  ------------------')

    input_crdf = '../tests/crds_test_files/big_list.csv'
    
    check_duplicate_rows_infile(input_crdf)
    
    check_duplicate_chords_infile(input_crdf)
    
    check_movable_chords_infile(input_crdf)

    print('\n-----------------------------------------------')
    