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


import libs.global_utilities as global_utilities
import libs.music_utilities as music_utilities


def test_frets_to_intervals(test_chords):
    # test_chords = ((chord_name, root_note, frets, assert_formula), ..)
    succeded_guesses = []
    failed_guesses = []
    for chord in test_chords:
        # chord =  ('Am', 'A', 'x,0,2,2,1,0', 'R, b3, 5')
        chord_name = chord[0] # 'Am'
        root_note = chord[1] # 'A'
        frets = chord[2] # 'x,0,2,2,1,0'
        frets_str = [elem.strip() for elem in frets.split(',')] #  ['x', '0', '2', '2', '1', '0']
        frets_int = global_utilities.crd_slst2ilst(frets_str) #   [None, 0, 2, 2, 1, 0]
        assert_frml = [elem.strip() for elem in chord[3].split(',')] # ['R', 'b3', '5']
        # grouping, not necessary
        assert_frml_set = set(assert_frml) # {'5', 'R', 'b3'}
        # guessed_intervals = [None, 'R', '5', 'R', 'b3', '5']
        guessed_intervals = music_utilities.frets_to_intervals(root_note, frets_int)
        # eliminate None -> ['R', '5', 'R', 'b3', '5']
        guessed_intervals = [elem for elem in guessed_intervals if elem]
        # grouping -> {'b3', '5', 'R'}
        guessed_frml_set = set(guessed_intervals)
        
        if guessed_frml_set.issubset(assert_frml_set):
            succeded_guesses.append((chord_name, assert_frml_set, guessed_frml_set, frets_int))
        else:
            failed_guesses.append((chord_name, assert_frml_set, guessed_frml_set, frets_int))
    return (succeded_guesses, failed_guesses)


def test_frets_to_intervals_form_file(input_crdf):
    linenumber = 0
    test_chords = []
    with open(input_crdf, mode='r') as infile:
        for infile_line in infile: 
            # strip start and final spaces:
            # A    A    x,0,2,2,2,0    x,x,1,2,3,x    maj    R, 3, 5
            infile_line_strip = infile_line.strip()
            linenumber += 1
            # make listelem list by tabs splitting
            # ['A', 'A', 'x,0,2,2,2,0', 'x,x,1,2,3,x', 'maj', 'R, 3, 5']
            listelem = infile_line_strip.split('\t')
            # strip single elements
            listelem = [elem.strip() for elem in listelem]
            # strip header line
            if linenumber > 1:
                chord_name = listelem[0] # 'A'
                root_note = listelem[1] # 'A'
                frets = listelem[2] # 'x,0,2,2,2,0'
                intervals_str = listelem[5] # 'R, 3, 5'
                test_chords.append((chord_name, root_note, frets, intervals_str))
    return test_frets_to_intervals(test_chords)    


if __name__ == "__main__":

    '''

    # test_chords = ((chord_name, root_note, frets, assert_formula), ..)
    test_chords = (
          ('Am', 'A', 'x,0,2,2,1,0', 'R, b3, 5')
        , ('B13sus2', 'B', 'x,2,4,2,2,4', 'R, 2, 5, b7, 11, 13')
        , ('G13sus4', 'G', '3,x,3,2,1,0', 'R, 4, 5, b7, 9, 13')
        , ('D5(#11)', 'D', 'x,x,0,2,3,4', 'R, 5, #11')
        , ('G6sus2', 'G', '3,0,0,0,3,0', 'R, 2, 5, 6')
        , ('G6sus4', 'G', '3,x,2,0,1,3', 'R, 4, 5, 6')
        , ('A9sus4', 'A', '5,x,5,4,3,0', 'R, 4, 5, b7, 9')
        , ('Badd11', 'B', '0,9,9,8,0,0', 'R, 3, 5, 11')
        , ('Aadd9', 'A', 'x,0,11,9,0,0', 'R, 3, 5, 9')
        , ('C+(add9)', 'C', 'x,3,2,1,3,0', 'R, 3, #5, 9')
        , ('Gdim9', 'G', '3,0,2,3,2,x', 'R, b3, b5, bb7, 9')
        , ('A11', 'A', '5,4,0,0,5,5', 'R, 3, 5, b7, 9, 11')
        , ('A13', 'A', '5,7,5,6,7,5', 'R, 3, 5, b7, 9, 11, 13')
        , ('A9', 'A', 'x,0,2,4,2,3', 'R, 3, 5, b7, 9')
        , ('Cmaj13', 'C', '5,7,5,5,5,7', 'R, 3, 5, 7, 9, 11, 13')
        , ('F#m11', 'F#', '2,0,2,2,0,0', 'R, b3, 5, b7, 9, 11')
        , ('C7b9', 'C', 'x,3,2,3,2,x', 'R, 3, 5, b7, b9')
        , ('G6(add9)', 'G', '3,0,2,2,0,0', 'R, 3, 5, 6, 9')
        , ('Am(add11)', 'A', 'x,0,0,2,1,0', 'R, b3, 5, 11')
        , ('Cmmaj11', 'C', 'x,3,1,4,1,1', 'R, b3, 5, 7, 9, 11')
        , ('C9#5', 'C', '8,7,6,7,x,6', 'R, 3, #5, b7, 9')
        , ('Cmaj9sus4', 'C', 'x,3,3,4,3,3', 'R, 4, 5, 7, 9')
        , ('Csus2(#11)', 'C', 'x,3,0,0,3,2', 'R, 2, 5, #11')
        , ('C9b5', 'C', 'x, 3, 2, 3, 3, 2', 'R, 3, b5, b7, 9')
        , ('Cmaj11', 'C', 'x, 3, 2, 0, 0, 1', 'R, 3, 5, 7, 9, 11')
        , ('C6', 'C', 'x,3,2,2,1,0', 'R, 3, 5, 6')
        , ('Bb6b5', 'Bb', 'x,1,0,0,3,0', 'R, 3, b5, 6')
        , ('Gmaj7(#11)', 'G', '3,2,0,0,2,2', 'R, 3, 5, 7, #11')
        , ('Dmaj9', 'D', 'x,5,2,2,2,2', 'R, 3, 5, 7, 9')
        , ('Cmaj9#5', 'C', '8, 7, 9, 7, 9, 7', 'R, 3, #5, 7, 9')
        , ('Gm13', 'G', '3,5,3,3,5,3', 'R, b3, 5, b7, 9, 11, 13')
        , ('Em6', 'E', '0,2,2,0,2,0', 'R, b3, 5, 6')
        , ('Cm6add9', 'C', 'x, 3, 1, 2, 3, 3', 'R, b3, 5, 6, 9')
        , ('Em9', 'E', '0,2,4,0,3,0', 'R, b3, 5, b7, 9')
        , ('Em(add9)', 'E', '0,2,4,0,0,0', 'R, b3, 5, 9')
        , ('Bmb6(add11)', 'B', 'x,2,4,0,3,0', 'R, b3, 5, b6, 11')
        , ('Cmmaj13', 'C', 'x, 3, 5, 4, 4, 5', 'R, b3, 5, 7, 9, 11, 13')
        , ('Cmmaj9', 'C', '8, 10, 9, 8, 8, 10', 'R, b3, 5, 7, 9')
    )

    (succeded_guesses, failed_guesses) = test_frets_to_intervals(test_chords)
    
    '''

    input_crdf = '../crds_test_files/test_frets2interv.txt'
    (succeded_guesses, failed_guesses) = test_frets_to_intervals_form_file(input_crdf)



    len_succeded = len(succeded_guesses)
    len_failed = len(failed_guesses)

    print('-----------------------------')
    print('OK: ' + str(len_succeded))
    print('KO: ' + str(len_failed))
    print('-----------------------------')
    if failed_guesses:
        print('Failed')
        for elem in failed_guesses:
            # failed_guesses = (chord_name, assert_frml_set, guessed_frml_set, frets_int)
            print(elem)
        print('-----------------------------')
