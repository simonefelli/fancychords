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
intervals: chord recognition, from frets to a chord name.

chord_finder(root_note, frets) is the entry point: it tries several
strategies and returns all the matches, best first. Every strategy turns
the frets into half-steps from the root and looks for that set of
half-steps in global_constants.formulas_list (formula_matcher):

    strategy      score  what it tries
    matcher        100   the chord as it is
    matcher_no5     90   the chord without the 5th
    slash           85   lowest note as slash note (ie D7/F#)
    slash_no5       70   slash chord without the 5th
    matcher_no3     60   the chord without the 3rd
    slash_no3       50   slash chord without the 3rd

A strategy loses 20 points when the bass note is not the root.
"""


# local application imports
from libs import global_constants
from libs import global_utilities
from libs import music_utilities
from libs import chords_formulas


def formula_matcher(hsteps_grpnormsort_lst, omitting_interv=None):
    '''
    given a grouped sorted and normalized half-steps list
    return: possible chord quality, formula list, grouped/sorted norm half-steps lists, maj/min quality
    this is accomplished by scanning for matches 'chords_formulas.formulas'
    expanding formulas when needed
    ie: f([0, 3, 5, 10], (5)) -> ('m11', ('R', 'b3', 'b7', '11'), (0, 3, 5, 10), (0, 3, 10, 5), 'minor')
    if there's no matching quality return None
    
    hsteps_grpnormsort_lst: List, grouped normalized and sorted half-steps list
    omitting_interv: Optional tuple, intervals to be erased in original formula
    
    return: Tuple, ( 
                     possible chord quality string
                   , chord quality formula list
                   , half-steps sorted and normalized formula tuple (also grouped, no repetitions)
                   , half-steps normalized formula tuple (also grouped, no repetitions)
                   , maj/min quality
                   )
    '''
    found_occurence = None
    # ie: name_frml = ('m11', ('R', 'b3', '5', 'b7', '(9)', '11'), 'minor')
    for name_frml in global_constants.formulas_list:
        if omitting_interv:
            # ie if omitting_interv = ('5') -> new_frml =  ('R', 'b3', 'b7', '(9)', '11')
            new_frml = chords_formulas.formula_omitter(name_frml[1], omitting_interv)
            # name_frml = ('m11', ('R', 'b3', 'b7', '(9)', '11'), 'minor')
            name_frml = (name_frml[0], new_frml, name_frml[2])
        # if now name_frml = ('6', ('R', '3', '(5)', '6'), 'major') then
        # formula_extender -> ((chord quality, formula_ext, half-steps sorted and normalized formula tuple,
        #                       half-steps and normalized formula tuple), ..., boolean variable if expanded)
        # =  (
        #      ('6', ('R', '3', '5', '6'), (0, 4, 7, 9), (0, 4, 7, 9), 'major')
        #    , ('6', ('R', '3', '6'), (0, 4, 9), (0, 4, 9), 'major')
        #    )
        # extend = True        
        name_frml_exp, extend = chords_formulas.formula_extender(name_frml)
        # no optional notes case: name_frml = ('6sus2', ('R', '2', '5', '6'), 'major') -> formula_extender() ->
        # name_frml_exp, extend = ('6sus2', ('R', '2', '5', '6'), (0, 2, 7, 9), (0, 2, 7, 9), 'major'), False
        if (not extend):
            # check if the two hsteps formulas match
            if hsteps_grpnormsort_lst == list(name_frml_exp[2]):
                found_occurence = name_frml_exp
                break
        # optional notes case
        else:
        # name_frml_exp, extend =
        # (
        #     ('m11', ('R', 'b3', 'b7', '9', '11'), (0, 2, 3, 5, 10), (0, 3, 10, 2, 5), 'minor')
        #   , ('m11', ('R', 'b3', 'b7', '11'), (0, 3, 5, 10), (0, 3, 10, 5), 'minor')
        # ), True
            for single_name_frml in name_frml_exp:
                # check if the two hsteps formulas match
                if hsteps_grpnormsort_lst == list(single_name_frml[2]):
                    found_occurence = single_name_frml
                    break
    return found_occurence


def check_bass_note_isroot(root_note, frets, flsh):
    '''
    given a root_note, a fret list and flat/sharp type, check if the first note from bottom string
    is the root_note. Returns a boolean falg showing if root is bass note
    and the bass note in 'flat'/'sharp' style
    ie: check_bass_note_isroot('C', [None,3,2,0,1,0], 'sharp') -> (True, 'C', [None,C',E',G',C',E'])
    ie: check_bass_note_isroot('C', [3,3,2,0,1,0], 'sharp') -> (False, 'G', ['G',C',E',G',C',E'])
    
    root_note: String, root note name
    frets: List, number fret list of a chord
    flsh: String, 'flat'/'sharp' style for output bass note
    
    return: Tuple, ( 
                     root_is_bass: Boolean, True if bottom note is root note
                   , bass_note: String, bass note in 'flat'/'sharp' style
                   , notes: List, notes string list
                   )
    '''
    # boolean flag
    root_is_bass = False
    # example for (D, [None, 0, 0, 2, 3, 2], sharp)
    # notes are [None, A, D, A, D, F#]
    # hsteps = [None, 7, 0, 7, 0, 4]  (normalized 1 octave)
    hsteps = music_utilities.frets_to_hsteps(root_note, frets)
    # get the first not None value from hsteps which is the lowest note in the chord
    # next() function returns the next item in an iterator.
    # if next() is applied only one time retuns first elem
    # first_hstep = 7
    first_hstep = next(elem for elem in hsteps if elem is not None)
    # as above get index of first not None value from hsteps
    # first_index = 1
    first_index = next(i for i in range(len(hsteps)) if hsteps[i] is not None)
    
    # chcek if bass note is root
    if first_hstep == 0: root_is_bass = True
    
    # get the notes list with correct enharmonic equivalent substitutions
    # following the half step rule of notes_validator() function
    notes = music_utilities.frets_to_valid_notes(frets, flsh)
    
    bass_note = notes[first_index]
 
    return root_is_bass, bass_note, notes


def frets_formula_matcher(root_note, frets, omitting_interv=None):
    '''
    given a root_note and a fret numbers list and an optional omitting tuple intervals, 
    if chord_quality is found:    
    return chord_quality, chord formula, a grouped-sorted half-steps
    list relative to root note, root_is_bass, bass_note, 'major'/'minor' formula quality,
    flsh of chord scale and notes list
    
    ie: frets_formula_matcher('A', [5, 4, 0, 0, 5, 5]) -> 
            ('maj11', ['R', '3', '11', 'b7', '5', 'R'], [0, 4, 5, 7, 10], True, 'A', 'major', 
             'sharp', ['A', 'C#', 'D', 'G', 'E', 'A'])
    
    if chord_quality is not found return:
    None for chord_quality, (root relative) note intervals list, half-steps list relative
    to root note, False for root_is_bass, bass_note and None for 'major'/'minor' quality,
    'sharp' and notes list
    ie: frets_formula_matcher('D', [1, 0, None, 2, 1, 2]) -> 
            (None, ['b3', '5', None, '5', 'b7', '3'], [3, 4, 7, 10], False, 'F', None, 'sharp',
             ['F', 'A', None, 'A', 'C', 'F#'])
    
    root_note: String, root note name
    frets: List, fret numbers list of a chord
    omitting_interv: Optional tuple, intervals to be erased in original formula
    
    return: Tuple, (
                  quality: String, chord_quality string
                , intervals_lst: List, chord formula list / list interval notation (if no match)
                , hsteps_grpnormsort_lst: List, half-steps list relative to root note (normalized and sorted)
                , root_is_bass: Boolean, True if bottom note is root note
                , bass_note: String, bass note
                , majmin: String, chord formula tonality: 'major'/'minor'
                , flsh: String, flat/sharp of chord based on music circle
                , notes: List, notes string list
                )    
    '''    
    quality = None
    intervals_lst = []
    # if (root_note, frets) = ('A', [5, 4, 0, 0, 5, 5])
    # hsteps_lst = [0, 4, 5, 10, 7, 0], hsteps_lst can have 'None's and is normalized to 1 octave
    hsteps_lst = music_utilities.frets_to_hsteps(root_note, frets)
    # hsteps_grpnormsort_lst = [0, 4, 5, 7, 10]
    hsteps_grpnormsort_lst = music_utilities.grpsort_hsteps_lst(hsteps_lst)
    # chord_quality = ('dom11', ('R', '3', '5', 'b7', '11'), (0, 4, 5, 7, 10), (0, 4, 7, 10, 5), 'major')
    chord_quality = formula_matcher(hsteps_grpnormsort_lst, omitting_interv)
    # get majmin from chord_quality, if chord_quality is not found: majmin -> None
    majmin = chord_quality[4] if chord_quality else None
    # if chord_quality is found desume if tonality is with flats or sharps for chord tones
    # throught the music circle and the majmin variable. For example if quality is maj7, we are
    # in a major contest, so for G -> sharp. If quality is min7, we are in a minor contest,
    # so for G -> flat (however for E would be sharp in every case).
    # if chord_quality is not found assume majmin = 'major'
    flsh = music_utilities.music_circle_flsh(root_note, majmin if majmin else 'major')
    # check if bass note is root
    # check_bass_note_isroot() -> True, 'A',  ['A', 'C#', 'D', 'G', 'E', 'A']
    root_is_bass, bass_note, notes = check_bass_note_isroot(root_note, frets, flsh)   
    # if a match is found
    if chord_quality:
        # quality = 'dom11'
        quality = chord_quality[0]
        # zip  (0, 4, 7, 10, 5), ('R', '3', '5', 'b7', '11') -> dict ->
        # steps_int_dict =  {0: 'R', 10: 'b7', 4: '3', 5: '11', 7: '5'}
        steps_int_dict = dict(list(zip(chord_quality[3], chord_quality[1])))
        # then associate found formula intervals to frets: hsteps_lst = [0, 4, 5, 10, 7, 0]
        # - > intervals_lst =  ['R', '3', '11', 'b7', '5', 'R']
        for elem in hsteps_lst:
            if elem is not None:
                intervals_lst.append(steps_int_dict[elem])
            else:
                intervals_lst.append(None)
    # if a match is not found
    else:
        quality = None
        # then simple associate root relative note intervals, to frets
        intervals_lst = music_utilities.hsteps_to_intervals(hsteps_lst)
    
    return quality, intervals_lst, hsteps_grpnormsort_lst, root_is_bass, bass_note, majmin, flsh, notes


def slash_chord_reducer(root_note, frets, flsh):
    '''
    given a root_note, a fret list and a flat/sharp type check if the first note from bottom string
    (6, string E bass) which is played can be a slash note candidate. 
    That happens if that note is not repeated on higher string (otherwise is just a voicing).
    returns 
    - True/False (valid slash note), 
    - slash note,
    - slash note half-step relative to root note,     
    - slash note interval relative to root note, 
    - slash note list index in original frets list,
    - fret list with first fret corresponding to slah note omitted and replaced by None

    ie: f(('A', [None, None, 4, 3, 3, 5])) -> (True, 'F#', 9, '6', 2, [None, None, None, 3, 3, 5])
        f(('A', [None, None, 2, 2, 2, 0])) -> (False, 'E', 7, '5', 2, [None, None, None, 2, 2, 0])
    
    root_note: String, root note name
    frets: List, number fret list of a chord
    flsh: String, flat/sharp type for slash note
    
    return: Tuple, ( 
                     real_slash: Boolean, True if bottom note can be a valid slash_note
                   , slash_note: String
                   , slash_note_hstep: Number, slash note half-steps relative to root note                   
                   , slash_note_interval: String, slash note interval relative to root note
                   , slash_fret_idx: Number, slash note index in original frets list
                   , trimmed_frets: List, fret list with omitted bottom fret and replaced by None
                   )
    '''
    real_slash = False
    # [None, None, 4, 3, 3, 5] -> notes = [None, None, 'F#', 'A#', 'D', 'A']
    notes = music_utilities.frets_to_notes(frets, flsh)
    slash_note = None
    slash_string = None
    slash_fret_idx = None   
    # [(0, None), (1, None), (2, 4), (3, 3), (4, 3), (5, 5)]
    for idx, frt in enumerate(frets):
        if frt is not None:
            slash_string = (6 - idx)
            slash_fret_idx = idx
            slash_note = music_utilities.singl_fret_to_note(slash_string, frt, flsh)
            break
    # half-steps interval of root_note -- slash_note
    slash_note_hstep = music_utilities.notes_to_hstep(root_note, slash_note)
    # interval of root_note -- slash_note
    slash_note_interval = music_utilities.hstep_to_interval(slash_note_hstep)
    #  sliced_frets = [3, 3, 5]
    sliced_frets = frets[(idx + 1):]
    # sliced_notes =  ['A#', 'D', 'A']
    sliced_notes = notes[(idx + 1):]
    # trimmed_frets = [None, None, None, 3, 3, 5]
    trimmed_frets = ((6 - len(sliced_frets)) * [None]) + sliced_frets
    # if candidate slash_note is not in sliced_notes then 
    # is a real slash note otherwise is just a voicing
    if slash_note not in sliced_notes: real_slash = True
    return (
          real_slash
        , slash_note
        , slash_note_hstep              
        , slash_note_interval
        , slash_fret_idx       
        , trimmed_frets
        )


def chrd_fndr_slshrdcr(root_note, frets, omitting_interv=None):
    '''
    given a root_note, a fret numbers list and an optional omitting tuple intervals,
    find chord_quality applying slash reducer first and then frets_formula_matcher
    
    If reducer is succesful and chord_quality is found, return 
    (chord_quality, chord_fulldetails, chord formula, half-steps list, root_is_bass, bass_note
        , majmin, flsh, notes)
    
    ie: chrd_fndr_slshrdcr('D', [1, None, 0, 2, 1, 2]) -> 
        ('7', '/F', ['b3',None,'R','5','b7','3'], [0,3,4,7,10], True, 'D', 'major', 'sharp', 
            ['F',None,'D','A','C','F#'])
    
    steps for match are: ('D', [1, None, 0, 2, 1, 2]) -> slash_chord_reducer -> 
        (True, 'F', 3, 'b3', 0, [None, None, 0, 2, 1, 2]) -> frets_formula_matcher -> 
        ('7', [None, None, 'R', '5', 'b7', '3'], [0, 4, 7, 10], True, 'D', 'major', ..) -> final ->
        ('7', '/F', ['b3',None,'R','5','b7','3'], [0,3,4,7,10], True, 'D', 'major', 'sharp', 
            ['F',None,'D','A','C','F#'])

    else return
    (None, None, intervals_lst, hsteps_grpnormsort_lst, root_is_bass, bass_note, None, flsh, notes)  
    
    steps for no match are: (D, [1, 0, None, 2, 1, 2]) -> slash_chord_reducer -> 
    (True, 'F', 3, 'b3', 0, [None, 0, None, 2, 1, 2])  -> frets_formula_matcher -> 
    (None, [None, '5', None, '5', 'b7', '3'], [4, 7, 10], False, 'A', None, ...) -> final ->
    (None, None, [None, '5', None, '5', 'b7', '3'], [4, 7, 10], False, 'A', None, 'sharp',
        [None, 'A', None, 'A', 'C', 'F#'])
    
    root_note: String, root note name
    frets: List, fret numbers list of a chord
    omitting_interv: Optional tuple, intervals to be erased in original formula
    
    return: Tuple, (
                      chord_quality: String, chord_quality string
                    , chord_fulldetails: String, chord_fulldetails string
                    , intervals_lst: List, chord formula list / list interval notation (if no match)
                    , hsteps_grpnormsort_lst:  List, half-steps list relative to root note (including slash note)
                    , root_is_bass: Boolean, True if bottom note is root note
                    , bass_note: String, bass note
                    , majmin: String, chord formula tonality: 'major'/'minor'
                    , flsh: String, flat/sharp of chord based on music circle
                    , notes: List, notes string list
                    )
    '''
    # for now make an assumption that slash_note is sharp
    flsh_hyp = 'sharp'
    
    # apply slash_chord_reducer
    # ('D', [1, None, 0, 2, 1, 2]) ->
    # slash_chord_reducer -> (True, 'F', 3, 'b3', 0, [None, None, 0, 2, 1, 2])
    (
      real_slash
    , slash_note
    , slash_note_hstep              
    , slash_note_interval
    , slash_fret_idx       
    , trimmed_frets
    ) = slash_chord_reducer(root_note, frets, flsh_hyp)

    # apply frets_formula_matcher on trimmed frets 
    # (slash note omitted) and check if there's a match
    # frets_formula_matcher ->
    # ('7', [None, None, 'R', '5', 'b7', '3'], [0, 4, 7, 10], True, 'D', 'major',
    # 'sharp', [None, None, 'D', 'A', 'C', 'F#'])
    (
          quality
        , intervals_lst
        , hsteps_grpnormsort_lst
        , root_is_bass
        , bass_note
        , majmin
        , flsh
        , notes
    ) = frets_formula_matcher(root_note, trimmed_frets, omitting_interv)
    
    # if it's a valid slash chord and a match is found
    if real_slash and quality:
        # check if slash_note is a valid slash: get valid_slashes list
        # to do so first get the notes from trimmed_frets and then
        # do the correct enharmonic substitutions with notes_validator()
        # slash_note = F
        # valid_slashes = ['C','D','E','Eb','F','F#','G','Gb','G#','A','B','Bb']
        slashes = music_utilities.frets_to_notes(trimmed_frets, flsh)
        valid_slashes = music_utilities.notes_validator(slashes)
        # if slash note is not valid then convert it flat <-> sharp
        if slash_note not in valid_slashes:
            reversed_slash_note = music_utilities.flsh_note_convers(slash_note)
            reversed_slash_note_interval = music_utilities.reverse_interv(slash_note_interval)
            # if converted slash_note is valid then this is the slash note
            # same applies for slash interval (#5 > b6)
            if reversed_slash_note in valid_slashes:              
                slash_note = reversed_slash_note
                slash_note_interval = reversed_slash_note_interval

        # change slash_note in notes list to match previous valid slash_note adjustment
        # slash_fret_idx = 0, slash_note = F
        # [None, None, 'D', 'A', 'C', 'F#'] -> ['F', None, 'D', 'A', 'C', 'F#']
        notes[slash_fret_idx] = slash_note
        
        # because chord is slashy, set the fulldetails string -> '/F'
        fulldetails = '/' + slash_note
        # make a copy of intervals_lst
        intervals_lst = list(intervals_lst)
        # append slash note interval
        # [None, None, 'R', '5', 'b7', '3'] -> ['b3', None, 'R', '5', 'b7', '3'] 
        intervals_lst[slash_fret_idx] = slash_note_interval
        # recompute hsteps_grpnormsort_lst:
        # append slash_note half-step to hsteps_grpnormsort_lst (not sorted)
        # [0, 4, 7, 10] -> [0, 4, 7, 10, 3]
        hsteps_grpnormsort_lst.append(slash_note_hstep)
        # usual stuff: grouping and sorting
        hsteps_grp_set = set(hsteps_grpnormsort_lst)
        hsteps_grpnormsort_lst = list(hsteps_grp_set)
        # [0, 3, 4, 7, 10]
        hsteps_grpnormsort_lst.sort()
    # else even slash_chord_reducer was succesful but frets_formula_matcher3
    # failed then quality = None, fulldetails = None
    else:
        quality = None
        fulldetails = None

    return  quality, fulldetails, intervals_lst, hsteps_grpnormsort_lst, \
            root_is_bass, bass_note, majmin, flsh, notes


def chord_finder(root_note, frets):
    '''
    given a root_note and a fret numbers list, find chord_quality applying 
    differente strategies. Each strategy has a score and produce a tuple like:
    (
        chord_quality, chord_fulldetails, bestchoice, 
        chord formula list, notes, hsteps_grpnormsort_lst, 
        plan_name, majmin, flsh, root_is_bass, bass_note
    )

    Return a list of all matching strategies.
    Higher score strategy should be preferred.
    ie: f((D, [6, None, 0, 2, 1, 2])) -> 
    [
      ('7(b13)', '/Bb', 80, ['b13',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], [0,4,7,8,10]
          , 'matcher', 'major', 'sharp', False, 'Bb'), 
      ('7', '/Bb', 85, ['#5',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], [0,4,7,8,10]
          , 'slash', 'major', 'sharp', True, 'D')
    ]
    , slash strategy (85) is the winner. 80 is matcher strategy (100) but root is not bass note (-20)
    
    if no math is found, return:
        [(None, None, 0, intervals_lst, notes, hsteps_grpnormsort_lst
        , None, None, None, root_is_bass, bass_note)]
    ie: [(None, None, 0, ['R','3','7','2','b5','7'], [None,'C','G','A#','D','G'], [0,2,4,6,11]
        , None, None, None, False, 'C')]
    
    
    root_note: String, root note name
    frets: List, fret numbers list of a chord
    
    return: List of tuple, all chord possibilities, higher score strategy is first:
        [
            ( chord_quality: String, chord_quality string
            , chord_fulldetails: String, chord_fulldetails string
            , bestchoice: Number, strategy score
            , intervals_lst: List, chord formula list / list interval notation (if no match)
            , notes: List, notes composing the chord
            , hsteps_grpnormsort_lst: List, half-steps list relative to root note (grouped, norm and sorted)
            , plan_name: String, strategy for actual choice
            , majmin: String, chord formula tonality: 'major'/'minor'
            , flsh: String, flat/sharp of chord based on music circle
            , root_is_bass: Boolean, True if bottom note is root note
            , bass_note: String, bass note
            ), 
            (
            ...
            ) ...
        ]        
    '''
    # boolean variable for found match
    found_match = False
    # list of tuple, each tuple is a startegy name and a score
    plans = [
          ('matcher', 100)
        , ('matcher_no5', 90)
        , ('slash', 85)
        , ('slash_no5', 70)
        , ('matcher_no3', 60)
        , ('slash_no3', 50)
        ]
    # helper variable for computing score
    bestchoice = 0
    fulldetails = ''
    # result list in the form of a list of tuple. A tuple for each possible match. A tuple is like:
    # (quality, fulldetails, bestchoice, intervals_lst, notes, hsteps_grpnormsort_lst, plan_name, 
    #  majmin, flsh, root_is_bass, bass_note)
    results = []
    # for each strategy
    for plan in plans:
        plan_name, plan_weight = plan  
        if plan_name == 'matcher':
            # simply try with frets_formula_matcher
            # for example (D, [6, None, 0, 2, 1, 2]) ->
            # ( 7(b13), ['b13', None, 'R', '5', 'b7', '3'], 
            #    [0, 4, 7, 8, 10], False, Bb, 'major', 
            #    'sharp', ['Bb', None, 'D', 'A', 'C', 'F#'])
            (
               quality
             , intervals_lst
             , hsteps_grpnormsort_lst
             , root_is_bass
             , bass_note
             , majmin
             , flsh
             , notes
            ) = frets_formula_matcher(root_note, frets)
            # keep the plain analysis of the chord: if no strategy matches,
            # it is what we return (see the end of the function). The other
            # strategies overwrite these variables with values computed on
            # trimmed frets (ie without the bass note)
            nomatch_result = (
                None, None, 0,
                intervals_lst, notes, hsteps_grpnormsort_lst,
                None, None, None,
                root_is_bass, bass_note)
            if quality:
                found_match = True
                # bestchoice = 100
                bestchoice = plan_weight
                # if root is not bass note decrease score by 20
                if not root_is_bass:
                    # bestchoice = 80
                    bestchoice = bestchoice - 20
                    # set fulldetails, (ie): 7(b13)/A# -> fulldetails = '/A#'
                    fulldetails = '/' + bass_note  
                # append the result
                # [
                #  ('7(b13)', '/Bb', 80, 
                #  ['b13',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], [0,4,7,8,10]
                #  'matcher', 'major', 'sharp',
                #   False, '/Bb')
                # ]
                results.append((
                    quality, fulldetails, bestchoice,
                    intervals_lst, notes, hsteps_grpnormsort_lst,
                    plan_name, majmin, flsh,
                    root_is_bass, bass_note))

        if plan_name == 'slash':
            # try assuming a slash chord
            # for example (D, [6, None, 0, 2, 1, 2]) ->
            # ( '7', '/Bb', ['#5', None, 'R', '5', 'b7', '3'], 
            #     [0,4,7,8,10], True, 'D', 'major', 'sharp', ['Bb',None,'D','A','C','F#'])            
            (
               slash_quality
             , slash_fulldetails
             , slash_intervals_lst
             , slash_hsteps_grpnormsort_lst
             , root_is_bass
             , bass_note
             , majmin
             , flsh
             , notes
            ) = chrd_fndr_slshrdcr(root_note, frets)
            # if a slash match is found
            if slash_quality:
                found_match = True
                quality = slash_quality
                fulldetails = slash_fulldetails
                intervals_lst = slash_intervals_lst
                hsteps_grpnormsort_lst = slash_hsteps_grpnormsort_lst
                # bestchoice = 85
                bestchoice = plan_weight
                # if root is not bass note decrease score by 20
                if not root_is_bass: bestchoice = bestchoice - 20            
                # append the result
                # [
                #    ('7', '/Bb', 85, ['#5',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], 
                #        [0,4,7,8,10], 'slash', 'major', 'sharp', True, 'D')
                #  , ('7(b13)', '/Bb', 80, ['b13',None,'R','5','b7','3'], ['Bb',None,'D','A','C','F#'], 
                #        [0,4,7,8,10], 'matcher', 'major', 'sharp', False, 'Bb')
                # ]
                results.append((
                    quality, fulldetails, bestchoice,
                    intervals_lst, notes, hsteps_grpnormsort_lst,
                    plan_name, majmin, flsh,
                    root_is_bass, bass_note))
        if plan_name == 'matcher_no5':
            # try then with frets_formula_matcher omitting 5th
            (
               no5_quality
             , no5_intervals_lst
             , no5_hsteps_grpnormsort_lst
             , root_is_bass
             , bass_note
             , majmin
             , flsh
             , notes
            ) = frets_formula_matcher(root_note, frets, ('5',))
            # if a match is found
            if no5_quality:
                found_match = True
                quality = no5_quality
                # fulldetails name is (no5)
                fulldetails = '(no5)'
                intervals_lst = no5_intervals_lst
                hsteps_grpnormsort_lst = no5_hsteps_grpnormsort_lst
                bestchoice = plan_weight
                # if root is not bass note decrease score by 20
                if not root_is_bass:
                    bestchoice = bestchoice - 20
                    # and quality name become (ie): Am(no5) -> Am(no5)/G
                    fulldetails = fulldetails + '/' + bass_note
                # append the result
                results.append((
                    quality, fulldetails, bestchoice,
                    intervals_lst, notes, hsteps_grpnormsort_lst,
                    plan_name, majmin, flsh,
                    root_is_bass, bass_note))
        if plan_name == 'slash_no5':
            # try assuming a slash chord and omitting 5th
            (
               slno5_quality
             , slno5_fulldetails
             , slno5_intervals_lst
             , slno5_hsteps_grpnormsort_lst
             , root_is_bass
             , bass_note
             , majmin
             , flsh
             , notes
            ) = chrd_fndr_slshrdcr(root_note, frets, ('5',))
            # if a slash match is found
            if slno5_quality:
                found_match = True
                # change quality name ie: Am/G -> Am/G(no5)
                quality = slno5_quality
                fulldetails = '(no5)' + slno5_fulldetails
                intervals_lst = slno5_intervals_lst
                hsteps_grpnormsort_lst = slno5_hsteps_grpnormsort_lst
                bestchoice = plan_weight
                # if root is not bass note decrease score by 20
                if not root_is_bass: bestchoice = bestchoice - 20
                # append the result
                results.append((
                    quality, fulldetails, bestchoice,
                    intervals_lst, notes, hsteps_grpnormsort_lst,
                    plan_name, majmin, flsh,
                    root_is_bass, bass_note))
        if plan_name == 'matcher_no3':
            # try with frets_formula_matcher omitting 3th
            (
               no5_quality
             , no5_intervals_lst
             , no5_hsteps_grpnormsort_lst
             , root_is_bass
             , bass_note
             , majmin
             , flsh
             , notes
            ) = frets_formula_matcher(root_note, frets, ('3',))
            # if a match is found
            if no5_quality:
                found_match = True
                # change quality name ie: Am -> Am(no3)
                quality = no5_quality
                fulldetails = '(no3)'
                intervals_lst = no5_intervals_lst
                hsteps_grpnormsort_lst = no5_hsteps_grpnormsort_lst
                bestchoice = plan_weight
                # if root is not bass note decrease score by 20
                if not root_is_bass:
                    bestchoice = bestchoice - 20 
                    # change quality name ie: Am(no3) -> Am(no3)/G
                    fulldetails = fulldetails + '/' + bass_note
                # append the result
                results.append((
                    quality, fulldetails, bestchoice,
                    intervals_lst, notes, hsteps_grpnormsort_lst,
                    plan_name, majmin, flsh,
                    root_is_bass, bass_note))
        if plan_name == 'slash_no3':
            # try assuming a slash chord and omitting 3th
            (
               slno3_quality
             , slno3_fulldetails
             , slno3_intervals_lst
             , slno3_hsteps_grpnormsort_lst
             , root_is_bass
             , bass_note
             , majmin
             , flsh
             , notes
            ) = chrd_fndr_slshrdcr(root_note, frets, ('3',))
            # if a slash match is found
            if slno3_quality:
                found_match = True
                # change quality name ie: Am/G -> Am/G(no3)
                quality = slno3_quality
                fulldetails = '(no3)' + slno3_fulldetails
                intervals_lst = slno3_intervals_lst
                hsteps_grpnormsort_lst = slno3_hsteps_grpnormsort_lst
                bestchoice = plan_weight
                # if root is not bass note decrease score by 20
                if not root_is_bass: bestchoice = bestchoice - 20
                # append the result
                results.append((
                    quality, fulldetails, bestchoice,
                    intervals_lst, notes, hsteps_grpnormsort_lst,
                    plan_name, majmin, flsh,
                    root_is_bass, bass_note))
    
    if found_match:
        # sorting return_list for bestchoice, ie: higher bestchoice first
        results = sorted(results, key=lambda x: x[2], reverse=True)
        return results
    else:
        # no match: return the plain analysis of the whole chord (from the
        # 'matcher' plan). It used to return notes, bass_note and
        # root_is_bass left over by the last plan ('slash_no3'), computed
        # without the bass note, ie for C [None,3,2,3,0,7] the bass note was
        # 'E' instead of 'C' and 'C' was missing from the notes
        results.append(nomatch_result)
        return results


if __name__ == "__main__":
    
    # testing these functions
    
    print('------------------  testing  ------------------')
    

    test_flsh = 'sharp'
    test_chord0 = [' 5', '4', '0', '0', '5 ', '5']
    test_chord1 = ('LA11', 'LA', global_utilities.crd_slst2ilst(test_chord0))
    hsteps_lst = music_utilities.frets_to_hsteps(test_chord1[1], test_chord1[2])
    hsteps_grpsort_lst = music_utilities.grpsort_hsteps_lst(hsteps_lst)

    print('\n- formula_matcher(' + str(hsteps_grpsort_lst) + '):\n\t', \
        formula_matcher(hsteps_grpsort_lst))
    
    print('\n- formula_matcher([0, 3, 5, 10], (''5'')):\n\t', formula_matcher([0, 3, 5, 10], ('5')))  

    print('\n- check_bass_note_isroot(' + test_chord1[1] + ', ' + str(test_chord1[2]) + ', ' + test_flsh + \
        '):\n\t', check_bass_note_isroot(test_chord1[1], test_chord1[2], test_flsh))  

    print('\n- check_bass_note_isroot(RE, [None, 0, 0, 2, 3, 2], sharp' + \
        '):\n\t', check_bass_note_isroot('RE', [None, 0, 0, 2, 3, 2], 'sharp')) 

    print('\n- frets_formula_matcher(' + test_chord1[1] + ', ' + str(test_chord1[2]) + '):\n\t', \
        frets_formula_matcher(test_chord1[1], test_chord1[2]))  
    
    print('\n- frets_formula_matcher(D, [None, 0, None, 2, 1, 2]):\n\t', \
        frets_formula_matcher('D', [None, 0, None, 2, 1, 2]))
    
    print('\n- frets_formula_matcher(RE, [None, None, 0, 2, 1, 2]):\n\t', \
        frets_formula_matcher('RE', [None, None, 0, 2, 1, 2])) 

    print('\n- frets_formula_matcher(RE, [1, 0, None, 2, 1, 2]):\n\t', \
        frets_formula_matcher('RE', [1, 0, None, 2, 1, 2])) 

    test_reducer = (
          ('LA', [None, None, 4, 3, 3, 5])   # -> True
        , ('A', [None, 0, 2, 2, 2, 0])      # -> False
        , ('RE', [1, None, 0, 2, 1, 2])      # -> True
        , ('LA', [5, 4, 0, 0, 5, 5])         # -> False
        , ('D', [1, 0, None, 2, 1, 2])      # -> True
        )
    
    for test in test_reducer:
        print('\n- slash_chord_reducer(' + test[0] + ', ' + str(test[1]) + '):\n\t', \
            slash_chord_reducer(test[0], test[1], test_flsh))

    test_slshrdcr = (
          ('RE', [1, None, 0, 2, 1, 2])   # -> True
        , ('A', [None, 0, 2, 2, 2, 0])   # -> False
        , ('RE', [6, None, 0, 2, 1, 2])   # -> True        
        , ('D', [1, 0, None, 2, 1, 2])   # -> False
        )

    for test in test_slshrdcr:
        print('\n- chrd_fndr_slshrdcr(' + test[0] + ', ' + str(test[1]) + '):\n\t', \
            chrd_fndr_slshrdcr(test[0], test[1]))

    print('\n- chord_finder((RE, [6, None, 0, 2, 1, 2])) ->\n\t', \
        chord_finder('RE', [6, None, 0, 2, 1, 2]))

    print('\n- chord_finder(D, [6,5,7,7,7,5]) -> D/Bb ->\n\t', \
        chord_finder('D', [6, 5, 7, 7, 7, 5]))

    print('\n- chord_finder(LA, [3,None,2,2,2,None]) -> A/G ->\n\t', \
        chord_finder('LA', [3, None, 2, 2, 2, None]))
    
    print('\n- chord_finder(D, [None,5,7,6,6,None]) -> Dm(maj7) ->\n\t', \
        chord_finder('D', [None,5,7,6,6,None]))

