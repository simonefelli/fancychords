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


from libs import global_utilities
from libs import music_utilities
from libs import intervals
from libs import chord_parser
from libs import import_tvk_json


def test_chord_finder(test_chords, quality_guess_adj, log_file):
    '''
    test intervals.chord_finder(root_note, frets) function against a list of
    chords (test_chords) and output a detailed log file (log_file)
    
    test_chords: List, list of chords to test in form of 
        [
          (chord_assert, root_note, frets_int, fingers,
           chord_assert_quality, chord_assert_detail, chord_assert_slash)
        , ...
        ]
    
    ie: [('Cm/C#', 'C', [None, 16, 17, 17, 17, None], ['x', '1', '2', '3', '4', 'x'], 'm', 'C#'), ...]
    
    quality_guess_adj: Tuple, search and replace strings adjustment for chord_assert_quality string
    in form of: ( (search_str, repl_str), ... )
        ie: ( ('major', ''), ('(no5)', '') ... )
    
    log_file: String, log file path
    
    return Nothing (log file is written)
    '''
    
    guesses = []    
    succeded_guesses = []
    failed_guesses = []
    
    # test_chords:
    # [(chord_assert, root_note, frets_int, fingers, chord_assert_quality, chord_assert_detail, chord_assert_slash), ..]
    # ('Gmaj7(no3)/C#', 'G', [3, None, 0, 0, 3, 2], ['2', 'x', 'x', 'x', '3', '1'], 'maj7', '(no3)', '/C#')
    
    for chord in test_chords:
        

        
        chord_assert, root_note, frets, fingers, \
            chord_assert_quality, chord_assert_detail, chord_assert_slash = chord
            
        # check if chords components are in latin notation
        # if so then convert them to english notation
        if music_utilities.is_latin_note(root_note): 
            root_note = music_utilities.conv_note_latin2en(root_note)
            if chord_assert_slash:
                chord_assert_slash = music_utilities.conv_note_latin2en(chord_assert_slash)
                chord_assert = root_note + chord_assert_quality + chord_assert_detail + \
                               '/' + chord_assert_slash
            else:
                chord_assert = root_note + chord_assert_quality + chord_assert_detail

        # chord_finder -> found_chords, each element is:
        # (quality, fulldetails, bestchoice, intervals_lst, notes, hsteps_grpsort_lst, 
        #  plan_name, majmin, flsh, root_is_bass, bass_note)
        # found_chords = [
        #    ('7', '/Bb', 85, ['#5',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], [0,4,7,8,10]
        #        , 'slash', 'major', 'sharp', True, 'D'), 
        #    ('7(b13)', '/Bb', 80, ['b13',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], [0,4,7,8,10]
        #        , 'matcher', 'major', 'sharp', False, 'Bb')
        # ]
        # if no math is found, return:
        # [(None, None, 0, intervals_lst, notes, hsteps_grpnormsort_lst
        #       , None, None, None, root_is_bass, bass_note)]
            
        found_chords = intervals.chord_finder(root_note, frets)
        # finder_first_quality = '7'
        finder_first_quality = found_chords[0][0]
        finder_output = []
        #  best_match_type variable goes higher for better guessing: 
        # 'perfect' -> 10, 'quality' -> 1, 'no_match' -> 0, 'finder_failed' -> -10
        # in the for loop, for each chord, best_match_type is summed up so a result
        # >= 10 means there is at least a 'perfect' match, a result > 0 and < 10
        # means one or more 'quality' match, a result = 0 means one or more 'no_match'
        # and a result < 0 means a 'finder_failed'.
        # ---
        # Result are appended to finder_output list
        # finder_output, each elem is: [ chord_guess, match_type, match ]
        # chord_guess = 'Cmaj7b5/D#', match_type = 'perfect'
        # match = ['maj7b5', '/D#', 65, [None,'b3','b5','R','3','7'], [None,'D#','F#','C','E','B'], 
        #            [0,3,4,6,11], 'slash', 'major', 'sharp', False, 'F#']
        # finder_output[x] = [
        #      'Cmaj7b5/D#'
        #    , 'perfect'
        #    , 'maj7b5', '/D#', 65, [None,'b3','b5','R','3','7'], [None,'D#','F#','C','E','B'], 
        #            [0,3,4,6,11], 'slash', 'major', 'sharp', False, 'F#'
        #    ]
        best_match_type = 0
        if finder_first_quality:
            for match in found_chords:
                # quality syntax adjustment for found_chords
                quality_guess = match[0]
                for (qserach, qreplace) in quality_guess_adj:
                    quality_guess = quality_guess.replace(qserach, qreplace, 1)
                # fulldetails_guess is for example '(no5)/Ab'
                fulldetails_guess = match[1]
                # 'Cmaj7b5/D#' = 'C' + 'maj7b5' + '/D#'
                chord_guess = root_note + quality_guess + fulldetails_guess
                # perfect chord match: 'Cmaj7b5/D#' = 'Cmaj7b5/D#'
                if (chord_guess == chord_assert):
                    match_type = 'perfect'
                    best_match_type += 10
                # quality match: 'Cm7#5/F#', 'Cm7#5/Gb': m7#5 = m7#5
                elif (quality_guess == chord_assert_quality): 
                    match_type = 'quality'
                    best_match_type += 1
                # no match: 'Caugmaj7' =! 'Cmaj7#5'
                else: match_type = 'no_match'
                finder_output.append([chord_guess] + [match_type] + list(match))
        else:
            # no match found append            
            # [[(None, None, 0, intervals_lst, notes, hsteps_grpnormsort_lst
            #        , None, None, None, root_is_bass, , bass_note)]]
            finder_output.append(found_chords)
            best_match_type = -10
        # guesses, each element is:
        # (
        #     (chord_assert, root_note, frets, fingers, chord_assert_quality, chord_assert_detail
        #    , chord_assert_slash)
        #    , best_match_type, finder_output
        # )
        # ie:
        # (
        #     ('Cmaj7b5/D#', 'C', [None, 6, 4, 5, 5, 7], ['x', '3', '1', '2', '4', '4'], 'maj7b5', ''
        #      , 'D#')
        #    , 'perfect', [
        #             ['Cmaj7b5/D#', 'perfect', 'maj7b5', '/D#', 65, [None ...]
        #           , ['Cmaj7b5(no5)/D#', 'quality', 'maj7b5', '(no5)/D#', 50, [None, ...]
        #          ]
        # )
        guesses.append(
            (
                (chord_assert, root_note, frets, fingers, chord_assert_quality,
                    chord_assert_detail, chord_assert_slash),
                best_match_type, finder_output)
            )

    for (ch_assert, best_match_type, finder_output) in guesses:
        
        if best_match_type >= 10:
            best_match = 'perfect'
        elif 0 < best_match_type < 10:
            best_match = 'quality'
        elif best_match_type == 0:
            best_match = 'no_match'
        elif best_match_type < 0:
            best_match = 'finder_failed'
        
        # xxx_guesses, each elem is: (ch_assert, best_match, finder_output)
        # each elem is:         
        # (
        #     ('Cmaj7b5/D#', 'C', [None, 6, 4, 5, 5, 7], 'maj7b5', '', 'D#')
        #    , 'perfect'
        #    [
        #          ['Cmaj7b5/D#', 'perfect', 'maj7b5', '/D#', 65, [None ...]
        #        , ['Cmaj7b5(no5)/D#', 'quality', 'maj7b5', '(no5)/D#', 50, [None, ...]
        #    ]
        # )
        
        if best_match_type > 0:
            succeded_guesses.append((ch_assert, best_match, finder_output))
        else:
            failed_guesses.append((ch_assert, best_match, finder_output))
    
    #  --- log file messages
    
    separator_1 = '\n#################################'
    separator_2 = '\n---------------------------------'
    separator_3 = '\n\n=========================================='
    
    # statistic for counting numbers per succesful match type (end of log file)
    succ_match_stats = {'perfect': 0, 'quality': 0, 'no_match': 0, 'finder_failed': 0}
    
    # statistic for counting numbers per failed match type (end of log file)
    fail_match_stats = {'perfect': 0, 'quality': 0, 'no_match': 0, 'finder_failed': 0} 
    
    # log number of Success
    
    msg_str = separator_1
    num_succ = '> Num Of Success: ' + str(len(succeded_guesses))
    print(num_succ)
    msg_str += '\n' + num_succ + separator_2

    # single succeded chord log
    for (ch_assert, best_match, finder_output) in succeded_guesses:
        succ_match_stats[best_match] += 1
        msg_str += '\nASSERT:\n* ' + str(ch_assert) + '\n' + 'GUESS: ' + str(best_match)
        for chord_guess in finder_output:
            msg_str += '\n* ' + str(chord_guess)
        msg_str += separator_2

    # log number of Failed

    num_fail = '> Num Of Failed: ' + str(len(failed_guesses))
    print(num_fail)
    msg_str += '\n' + separator_1 + '\n' + num_fail + separator_2
    
    # single failed chord log
    for (ch_assert, best_match, finder_output) in failed_guesses:
        fail_match_stats[best_match] += 1
        msg_str += '\nASSERT:\n* ' + str(ch_assert) + '\n' + 'GUESS: ' + str(best_match)
        for chord_guess in finder_output:
            msg_str += '\n* ' + str(chord_guess)
        msg_str += separator_2

    # summary end stats

    msg_str += separator_3 + '\n\n' + \
        num_succ + '\n' + str(succ_match_stats) + \
        '\n\n' + num_fail + '\n' + \
        str(fail_match_stats)

    # deeper stats on failed_guesses
    
    failed_study = {}
    finder_failed_study = {}
    for (ch_assert, best_match, finder_output) in failed_guesses:
        chord_assert_quality = ch_assert[4]
        if chord_assert_quality in failed_study:
            failed_study[chord_assert_quality] += 1
        else:
            failed_study[chord_assert_quality] = 1
        if best_match == 'finder_failed':
            if chord_assert_quality in finder_failed_study:
                finder_failed_study[chord_assert_quality] += 1
            else:
                finder_failed_study[chord_assert_quality] = 1    
    
    # sorting per number of occorences desc
    # failed_study = {'aug9': 8, 'majb5': 12, 'augmaj9': 9, 'm#5': 12, ....}
    # list(finder_failed_study.items()) = [('aug9', 8), ('majb5', 12), ('augmaj9', 9), ('m#5', 12)]
    # -> sort() -> [('majb5', 12), ('m#5', 12), ('augmaj9', 9), ('aug9', 8)]
    sort_failed_study = sorted(list(failed_study.items()), key=lambda x: x[1], reverse=True)
    sort_finder_failed_study = sorted(list(finder_failed_study.items()), key=lambda x: x[1], reverse=True)
    
    msg_str += '\n\n> Failed Asserts: ' + str(sort_failed_study)
    msg_str += '\n\n> Failed Finder: ' + str(sort_finder_failed_study)
    msg_str += separator_3
    
    print('Job Done! See details in: ' + log_file)
    
    f1 = open(log_file, 'w')
    f1.write(msg_str)
    f1.close()


def mybig_list_file_to_test_chords(input_crdf):
    '''
    turn an input chord file in style
    
        NAME   FRETS          FINGERS          DOT LABELS      FOOTER          SUBFOLDER
        DO     X,3,2,0,1,0    X,3,2,X,1,X      X,R,3,5,R,3     X,3,2,X,1,X     Major  
    
    into test_chords list
    
    [(chord_assert, root_note, frets_int, fingers, chord_assert_quality, chord_assert_detail, chord_assert_slash), ..]
    [('Gmaj7(no3)/C#', 'G', [3, None, 0, 0, 3, 2], ['2','x','x','x','3','1'], 'maj7', '(no3)', '/C#'), ...]
    
    input_crdf: String, input file path
                only chord_name, frets are mandatory, if a non mandatory parameters 
                is to be given but some preceding ones are to be skipped use '%'
    
    return: List, test_chords
    '''
    
    test_chords = []    
    
    crd_list = chord_parser.get_crd_list_from_file(input_crdf, print_output=False)[0]
    
    # crd_list = [
    #   [
    #      chord_name
    #    , root_note
    #    , chord_filename
    #    , frets
    #    , fingers
    #    , dlabels
    #    , footer
    #    , subfolder
    #    , chord_quality
    #    , chord_detail
    #    , chord_slash
    #   ]
    # , [...
    # ]

    for crd in crd_list:
        chord_assert = crd[0]
        root_note = crd[1]
        frets = global_utilities.crd_slst2ilst(crd[3])     
        fingers = crd[4]           
        chord_assert_quality = crd[9]
        chord_assert_detail = crd[10]
        chord_assert_slash = crd[11]
             
        test_chords.append(
            (chord_assert, root_note, frets, fingers, 
             chord_assert_quality, chord_assert_detail, chord_assert_slash)
            )
    
    return test_chords


def tvk_json_file_to_test_chords(input_jsonf):
    '''
    turn a tvk json input chord file in style
    
    {
      "Cmaj7b5/D#":[{"positions":["x","6","4","5","5","7"],"fingerings":[["0","3","1","2","4","4"]]}]
    , "Cm11/F":[{"positions":["1","1","1","0","1","x"],"fingerings":[["1","2","3","0","4","0"]]}]
    }
    
    into test_chords list
    
    [(chord_assert, root_note, frets_int, fingers, chord_assert_quality, chord_assert_detail, chord_assert_slash), ..]
    [('Gmaj7(no3)/C#', 'G', [3, None, 0, 0, 3, 2], ['2','x','x','x','3','1'], 'maj7', '(no3)', '/C#'), ...]
    
    input_jsonf: String, input tvk json
    
    return: List, test_chords
    '''
    
    # crd_json_file_list = [[chord_name, frets, fingers, '%', '%', dirout], ..]
    crd_json_file_list = import_tvk_json.parse_tvk_json_file(input_jsonf)[1]
    
    # get_crd_list_from_str_list() -> (crd_list, msg_str)
    # crd_list = [
    #   [
    #      chord_name
    #    , root_note
    #    , chord_filename
    #    , frets, fingers
    #    , dlabels
    #    , footer
    #    , subfolder
    #    , chord_quality
    #    , chord_detail
    #    , chord_assert_slash
    #   ]
    # , [...
    # ]
    crd_list = chord_parser.get_crd_list_from_str_list(crd_json_file_list, print_output=False)[0]

    # test_chords:
    # [(chord_assert, root_note, frets_int, fingers, chord_assert_quality
    #  , chord_assert_detail, chord_assert_slash), ..]
    #  [('Gmaj7(no3)/C#', 'G', [3, None, 0, 0, 3, 2], ['2','x','x','x','3','1'], 'maj7', '(no3)', '/C#'), ...]
    test_chords = []   
    
    for crd in crd_list:
        chord_assert = crd[0]
        root_note = crd[1]
        frets = global_utilities.crd_slst2ilst(crd[3])
        fingers = crd[4]
        chord_assert_quality = crd[9]
        chord_assert_detail = crd[10]
        chord_assert_slash = crd[11]
        test_chords.append(
            (chord_assert, root_note, frets, fingers,
             chord_assert_quality, chord_assert_detail, chord_assert_slash)
            )

    return test_chords


def test_chord_finder_on_mybig_list_file(input_crdf, log_file):
    '''
    given mybig chord file in input, test it with 
    intervals.chord_finder(root_note, frets) function
    and output a detailed log file (log_file)
    
    input_crdf: String, mybig chord list input file in style
        NAME   FRETS          FINGERS          DOT LABELS      FOOTER          SUBFOLDER
        DO     X,3,2,0,1,0    X,3,2,X,1,X      X,R,3,5,R,3     X,3,2,X,1,X     Major  
    log_file: String, log file path
    
    return Nothing (log file is written)
    '''
    
    test_chords = mybig_list_file_to_test_chords(input_crdf)
    
    # adjustment for quality_guess:
    # 'major' -> '' so 'Abmajor/F#' -> 'Ab/F#'
    quality_guess_adj = (
          ('major', ''),
        )
    
    print('\nChecking: ', input_crdf)
    test_chord_finder(test_chords, quality_guess_adj, log_file)


def test_chord_finder_on_tvk_json_file(input_jsonf, log_file):
    '''
    given tvk_json chord file in input, test it with 
    intervals.chord_finder(root_note, frets) function
    and output a detailed log file (log_file)
    
    input_jsonf: String, input tvk json in style
    {
      "Cmaj7b5/D#":[{"positions":["x","6","4","5","5","7"],"fingerings":[["0","3","1","2","4","4"]]}]
    , "Cm11/F":[{"positions":["1","1","1","0","1","x"],"fingerings":[["1","2","3","0","4","0"]]}]
    }
    log_file: String, log file path
    
    return Nothing (log file is written)
    '''
    
    test_chords = tvk_json_file_to_test_chords(input_jsonf)
    
    # adjustment for quality_guess:
    # 'major' -> '',  '(no5)' -> ''
    # so 'Abmajor(no5)/F#' -> 'Ab/F#'
    quality_guess_adj = (
          ('major', '')
        , ('(no5)', '')
        , ('(', '')
        , (')', '')
        , ('+', 'aug')
        )
    
    print('\nChecking: ', input_jsonf)
    test_chord_finder(test_chords, quality_guess_adj, log_file)
    


if __name__ == "__main__":

    '''

    input_crdf = '../crds_test_files/small_list_ita.csv'       # full path for big_list chord file
    log_file = './log_small_list.txt'
    test_chord_finder_on_mybig_list_file(input_crdf, log_file)



    input_crdf = '../crds_test_files/big_list.csv'       # full path for big_list chord file
    log_file = './log_big_list.txt'
    test_chord_finder_on_mybig_list_file(input_crdf, log_file)
    
    '''

    input_jsonf = '../misc_tests_files/tvk_all_c.json'       # full path for tvk json chord file
    log_file = './log_tvk_all_c.txt'
    test_chord_finder_on_tvk_json_file(input_jsonf, log_file)

