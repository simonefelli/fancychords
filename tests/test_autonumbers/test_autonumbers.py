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


from libs import autofingers
from libs import global_utilities


def test_frets_str2lst(test_chords):
    '''
    from chords tuples input string form ie: 
    ('DO', 'X,3,2,0,1,0', 'X,3,2,X,1,X'), ... -> 
    ('DO', ['x','3','2','0','1','0'], ['x','3','2','x','1','x']), ...
    '''
    test_frets = []
    for chord in test_chords:
        chord_name = chord[0]
        frets_str = chord[1]
        fingers_str = chord[2]
        frets_slst = global_utilities.crd_str2slst(frets_str)
        fingers_slst = global_utilities.crd_str2slst(fingers_str)
        test_frets.append((chord_name, frets_slst, fingers_slst))
    return test_frets


def test_autofingers_form_file(input_crdf):
    '''
    from chords string in text file ie: ('DO     X,3,2,0,1,0       X,3,2,X,1,X'), ....
    turn them in tuples ie: ('DO', 'X,3,2,0,1,0', 'X,3,2,X,1,X'), ...
    '''
    linenumber = 0
    test_frets = []
    with open(input_crdf, mode='r') as infile:
        for infile_line in infile: 
            # strip start and final spaces
            infile_line_strip = infile_line.strip()
            linenumber += 1
            # make listelem list by tabs splitting
            listelem = infile_line_strip.split('\t')
            # strip single elements
            listelem = [elem.strip() for elem in listelem]
            # strip header line
            if linenumber > 1:
                chord_name = listelem[0]
                frets = listelem[1]
                fingers = listelem[2]
                test_frets.append((chord_name, frets, fingers))
    return test_frets


def test_autofingers(test_frets):
    '''
    test autofinger function using assert/guess logic
    
    test_frets, tuple of tuple: ((chord_name, chord_frets, fingers_assert), ..)
    ie: (('C', ['x','3','2','0','1','0'], ['x', '3', '2', 'x', '1', 'x']), ...)
    
    return: print log
    '''
    succeded_guesses = []
    failed_guesses = []
    for frets_str in test_frets:

        chord_name, chord_frets, test_assert = frets_str
        test_guess = autofingers.chord_autofingers(chord_frets) 
        if test_assert == test_guess:
            succeded_guesses.append((chord_name, chord_frets, test_assert, test_guess))
        else:
            failed_guesses.append((chord_name, chord_frets, test_assert, test_guess))

    len_succeded = len(succeded_guesses)
    len_failed = len(failed_guesses)
    
    print('----  Info Tests  ----------------')
    for chord_name, chord_frets, test_assert, test_guess in failed_guesses:
        print('chord_name:\t', chord_name)
        print('chord_frets:\t', chord_frets)
        print('Assert:\t\t', test_assert)
        print('Guess:\t\t', test_guess)
        print('--------------------------------')

    print('OK: ' + str(len_succeded))
    print('KO: ' + str(len_failed))
    print('----------------------------------')


if __name__ == "__main__":


    
    test_frets = (
          ('C',          ['x','3','2','0','1','0'], ['x', '3', '2', 'x', '1', 'x'])
        , ('C/G',        ['3','3','2','0','1','0'], ['3', '4', '2', 'x', '1', 'x'])
        , ('Fmaj7',      ['0','3','3','2','1','x'], ['x', '3', '4', '2', '1', 'x'])
        , ('B',          ['x','2','4','4','4','2'], ['x', '1', '2', '3', '4', '1'])
        , ('Bm',         ['x','2','4','4','3','2'], ['x', '1', '3', '4', '2', '1'])
        , ('Dm7',        ['x','x','x','2','1','1'], ['x', 'x', 'x', '3', '1', '2'])
        , ('E/G#',       ['4','x','2','4','5','x'], ['2', 'x', '1', '3', '4', 'x'])
        , ('Dm7b5',      ['x','5','6','5','6','x'], ['x', '1', '3', '2', '4', 'x'])
        , ('D',          ['x','x','0','2','3','2'], ['x', 'x', 'x', '1', '3', '2'])
        , ('G13',        ['3','x','3','4','5','x'], ['1', 'x', '2', '3', '4', 'x'])
        , ('E7(#9)',     ['0','7','6','7','8','x'], ['x', '2', '1', '3', '4', 'x'])
        , ('E7(#9,b13)', ['0','7','6','7','8','8'], ['x', '2', '1', '3', '4', '4'])
        , ('F/G',        ['3','x','3','2','1','x'], ['3', 'x', '4', '2', '1', 'x'])
        , ('G6',         ['3','x','2','4','3','x'], ['2', 'x', '1', '4', '3', 'x'])
        , ('GX',         ['3','x','2','3','2','2'], ['2', 'x', '1', '3', '1', '1'])
        , ('E9',         ['x','7','6','7','7','7'], ['x', '2', '1', '3', '3', '3'])
        , ('E9b13',      ['x','7','6','7','7','8'], ['x', '2', '1', '3', '3', '4'])
        , ('XY',         ['3','3','5','5','6','6'], ['1', '1', '2', '2', '3', '4'])
        )
    
    '''
    
    input_crdf = '../crds_test_files/big_list.csv'
    test_chords = test_autofingers_form_file(input_crdf)
    test_frets = test_frets_str2lst(test_chords)
    
    '''
    
    test_autofingers(test_frets)
    