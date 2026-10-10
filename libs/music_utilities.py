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


# local application imports
from libs import global_constants
from libs import global_utilities
from libs import chord_parser
from libs import autofingers


def isnote_flsh(note):
    '''
    tells if a note is a flat or sharp. For natural notes default to 'sharp'
    ie: isnote_flsh('Ab') -> 'flat', isnote_flsh('G') -> 'sharp'
    
    note: String, note name
    
    return String, note accident type 'flat'/'sharp'
    '''
    note = normalize_note_name(note)
    # check if root_note is in latin notation then convert it to english notation
    if is_latin_note(note): note = conv_note_latin2en(note)
    # sharp_chrscale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # flat_chrscale = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    if note in global_constants.sharp_chrscale:
        return 'sharp'
    elif note in global_constants.flat_chrscale:
        return 'flat'


def is_latin_note(note):
    '''
    check if a note is in latin notation
    ie: is_latin_note(C#) -> False
        is_latin_note(SOLb) -> True
        
    note: String, note name
    
    return Boolean, check result
    '''
    is_latin = False
    natural_note = ''
    # check for flat or sharps in last letter
    if note[-1] in ('b', '#'):
        natural_note = note[:-1]
    else:
        natural_note = note
    # notes_latin = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
    if natural_note in global_constants.notes_latin: is_latin = True
    return is_latin
        

def conv_note_latin2en(latin_note):
    '''
    turn latin root note name in a chord to english notation
    ie: conv_note_latin2en('SOLb') -> 'Gb'
    
    latin_note: String, note latin name
    
    return: String, note name with flat or sharps in english notation
            return None if note was not in latin notation
    '''
    # notes_eng = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    # conversion dict, ie: {'DO': 'C', 'LA': 'A', 'MI': 'E', ...}
    latin2en_dict = dict(list(zip(global_constants.notes_latin, global_constants.notes_eng)))
    # note without flat or sharps
    latin_natural_note = ''
    # check for flat or sharps
    if latin_note and (latin_note[-1] in ('b', '#')):
        latin_natural_note = latin_note[:-1]
        sharp_flat = latin_note[-1]
    else:
        latin_natural_note = latin_note
        sharp_flat = ''
    # notes_latin = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
    if latin_natural_note in global_constants.notes_latin:
        return latin2en_dict[latin_natural_note] + sharp_flat
    else:
        return None
    

def conv_note_en2latin(en_note):
    '''
    turn english root note name in latin notation note
    ie: conv_note_en2latin('Gb') -> 'SOLb'
    
    english_note: String, note english name
    
    return: String, note name with flat or sharps in latin notation
            return None if note was not in english notation
    '''
    # notes_latin = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
    # conversion dict, ie: {'C': 'DO', 'A': 'LA', 'E': 'MI', ...}
    en2latin_dict = dict(list(zip(global_constants.notes_eng, global_constants.notes_latin)))
    # note without flat or sharps
    en_natural_note = ''
    # check for flat or sharps
    if en_note and (en_note[-1] in ('b', '#')):
        en_natural_note = en_note[:-1]
        sharp_flat = en_note[-1]
    else:
        en_natural_note = en_note
        sharp_flat = ''
    # notes_eng =   ['C',  'D',  'E',  'F',  'G',   'A',  'B' ]
    if en_natural_note in global_constants.notes_eng:
        return en2latin_dict[en_natural_note] + sharp_flat
    else:
        return None


def conv_chordname_en2latin(en_chordname):
    '''
    turn english chord name into a latin notation chord
    ie: conv_chordname_en2latin('Cm7/G#') -> 'SOLb'
    
    en_chordname: String, chord english name
    
    return: String, chord name in latin notation
            return None if note was not in english notation
    '''
    root_note, quality, detail, slash_note = chord_parser.parse_chord_name(en_chordname)
    latin_root_note = conv_note_en2latin(root_note)
    latin_slash_note = '/' + conv_note_en2latin(slash_note) if slash_note else ''
    latin_chord_name = latin_root_note + quality + detail + latin_slash_note
    return latin_chord_name





def normalize_note_name(note):
    '''
    turn note name (with flat or sharps) to uppercase
    note name can also be in latin notation
    ie: normalize_note_name('f#') ->  'F#'
        normalize_note_name('fa#') -> 'FA#'
    
    note: String, note name
    
    return String, note name to uppercase
    '''
    # check for flat or sharps in last letter
    if note[-1] in ('b', '#'):
        return note[:-1].upper() + note[-1]
    else:
        return note.upper()


def flsh_note_convers(note):
    '''
    convert a note from sharp <-> flat
    ie: flsh_note_convers('F#') -> 'Gb'
    
    note: String, note name
    
    return String, converted note
    '''
    # note = f# -> F#
    note = normalize_note_name(note)
    # check if root_note is in latin notation then convert it to english notation
    if is_latin_note(note): note = conv_note_latin2en(note)
    # 'sharp'
    flsh_type_for_note = isnote_flsh(note)
    # flsh_chrscale['sharp'] -> sharp_chrscale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', ...]
    # flsh_chrscale['flat']  -> flat_chrscale =  ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', ...]
    # note_index = 6
    note_index = global_constants.flsh_chrscale[flsh_type_for_note].index(note)    
    if flsh_type_for_note == 'sharp':
        return global_constants.flsh_chrscale['flat'][note_index]
    elif flsh_type_for_note == 'flat':
        return global_constants.flsh_chrscale['sharp'][note_index]


def music_circle_flsh(note, majmin):
    '''
    given a root note and a maj/min tonality return correspondig note circle
    accident type: 'flat' or 'sharp'
    ie: music_circle('G', 'major') -> 'sharp'
        music_circle('G', 'minor') -> 'flat'
    
    note: String, root note name
    majmin: String, tonality: 'major'/'minor'
    
    return String, note accident type 'flat'/'sharp'
    '''
    note = normalize_note_name(note)
    # check if root_note is in latin notation then convert it to english notation
    if is_latin_note(note): note = conv_note_latin2en(note)
    if majmin == 'major':
        # major_music_circle = {'C': ('sharp', 0), 'G': ('sharp', 1), ..., 'F': ('flat', 1),, ... 
        return global_constants.major_music_circle[note][0]
    elif majmin == 'minor':
        # minor_music_circle = {'A': ('sharp', 0), 'E': ('sharp', 1), ..., 'D': ('flat', 1), ...
        return global_constants.minor_music_circle[note][0]
    

def n_octaves(root_note, num_octave, flsh):
    '''
    Given a root note, a number of octaves to be displayed and a 'flat'/'sharp' type
    return a chromatic scale in a list for that note. The scale is 'flat' or 'sharp'
    depending on flsh. The scale extends for number of octaves
    ie: n_octaves('F#', 1, 'sharp') -> ['F#','G','G#','A','A#','B','C','C#','D','D#','E','F']
    ie: n_octaves('F#', 1, 'flat')  -> ['Gb','G','Ab','A','Bb','B','C','Db','D','Eb','E','F']
    
    root_note: String, root_note name
    num_octave: Number extent of scale in terms of octaves
    flsh: String, 'flat'/'sharp' type of output chromatic scale
    
    return List of chromatic scale (for num_octave octaves) for root_note
    '''
    root_note = normalize_note_name(root_note)
    # check if root_note is in latin notation then convert it to english notation
    if is_latin_note(root_note): root_note = conv_note_latin2en(root_note)
    # root_note is flat or sharps?
    flsh_type_for_root_note = isnote_flsh(root_note)
    # if root_note flat/sharps is not the same of required flsh
    # then convert root_note type, ie: root_note = 'F#', flsh = 'flat 'then 'F#' -> 'Gb'
    if flsh_type_for_root_note != flsh:
        root_note = flsh_note_convers(root_note)
    # take a flat/sharp chromatic scale for (num_octave + 1) octaves starting from C
    # flsh_chrscale['sharp'] -> sharp_chrscale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', ...]
    # flsh_chrscale['flat']  -> flat_chrscale =  ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', ...]
    my_octaves = global_constants.flsh_chrscale[flsh] * (num_octave + 1)
    # find index list for first occurence of root_note = 6 (first F#)
    root_index = my_octaves.index(root_note)
    # now slice my_octaves for final result
    n_octaves = my_octaves[root_index: (root_index + (num_octave * 12))]
    return n_octaves


def swap_flat_sharp(flsh):
    '''
    Simply swap 'flat' <-> 'sharp'
    
    flsh: String, can be 'flat' or 'sharp'
    
    return: String, swapped flsh
    '''
    swapped = None
    swap_dict = {
          'flat': 'sharp'
        , 'sharp': 'flat'
        }
    if flsh in swap_dict:
        swapped = swap_dict[flsh]
    return swapped


def reverse_interv(interv):
    '''
    given a string interval return its enharmonic equivalent, for
    natural interval (no flats or sharps) return original interval:
    #6 -> b7, 4 -> 4
    
    interv: String, interval in string notation
    
    return: String, enharmonic interval or original interval if natural
    '''
    found_int = interv
    # reverse_interv_dict = {'b3': '#2', 'b5': '#4', 'b6': '#5', ...
    for key, val in global_constants.reverse_interv_dict.items():
        if interv == key:
            found_int = val
            break
        elif interv == val:
            found_int = key
            break
    return found_int


def quality_to_majmin(chord_quality):
    '''
    given a chord quality return chord tonality 'major'/'minor'
    ie: quality_to_majmin(mb6(Add11)) -> 'minor'
    
    chord_quality: String, chord_quality string
    
    return majmin: String, chord formula tonality: 'major'/'minor'
    '''
    # normalize chord_quality to lowercase
    chord_quality = chord_quality.lower()
    # use next() to find first sequence item that matches a criterion
    # get None if item is not found
    # formulas_list = (('5', ('R', '5'), 'major'), ('5(#11)', ('R', '5', '#11'), 'major'), ...
    majmin = next(
          (formula[2] for formula in global_constants.formulas_list if formula[0] == chord_quality)
        , None
        )
    return majmin


def is_latin_chord(chord):
    '''
    check if a chord is in latin notation and return also its eng name
    ie: is_latin_chord(LAadd9/MI) -> (True, 'Aadd9/E')
        is_latin_chord(SOLb/REb) ->  (True, 'Gb/Db')
        is_latin_chord(B7/F#)  ->    (False, 'B7/F#')
        
    note: String, chord name
    
    return: Tuple
    - Boolean, check result
    - Converted eng name (if needed)
    '''
    is_latin = False
    
    root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord)
    if is_latin_note(root_note):
        is_latin = True
        root_note = conv_note_latin2en(root_note)
        if slash_note: slash_note = conv_note_latin2en(slash_note)
    if is_latin: chord = root_note + quality + detail + '/' + slash_note
    return (is_latin, chord)


def lowest_root_in_chord(chord_name, frets_int):
    '''
    given chord_name and frets_int 
    return lowest string (from 6 to 1) in which root note is present
    
    ie: (Dbmaj7, [None, 4, 6, 5, 6, 0]) -> 5
    '''
    # parse_chord_name(F#m(no5)/Gb) -> ('F#', 'm', '(no5)', 'Gb')
    parsed_chord_name = chord_parser.parse_chord_name(chord_name)
    root_note, quality = parsed_chord_name[0], parsed_chord_name[1]
    # for a major chord quality is '' so replace it with 'major'
    if not quality: quality = 'major'
    # mb6(Add11) -> 'minor'
    majmin = quality_to_majmin(quality)
    # chord is flat or sharp throughout music circle based on root_note, majmin    
    flsh_root = music_circle_flsh(root_note, majmin)
    # ([None, 4, 6, 5, 6, 4], 'flat') -> [None, 'Db', 'Ab', 'C', 'F', 'Ab']
    notes = frets_to_notes(frets_int, flsh_root)
    # use next() to find first sequence item that matches a criterion
    # get None if item is not found
    # string numbers go from 6 to 1 so (6-0) to (6-5)
    lowest_root_string = next(
          ((6-idx) for idx, note in enumerate(notes) if note == root_note)
        , None
        )
    return lowest_root_string


def chord_normalize(frets):
    '''
    given frets and fingers, check if chord form is movable using frets_int_normalize function
    ie: Dbmaj7 -> chord_normalize(['x','4','6','5','6','4']) -> (True, [None, 1, 3, 2, 3, 1], 3)
    
    frets: List of strings, fret sequence, ie ['x','4','6','5','6','4']
    fingers: List of strings, finger numbers list, ie ['x','1','2','3','4','1']
    
    return Tuple:
    - is_movable_form: Boolean, True if chord form is movable
    - frets_int_norm: List, number fret list of a chord, ie [None,1,3,2,3,1]
    - offset half-steps used to normalize
    '''
    frets_int = global_utilities.crd_slst2ilst(frets)
    # frets_int_normalize([None, 4, 6, 5, 6, 4]) -> (True,  [None, 1, 3, 2, 3, 1], 3)
    is_movable_form, frets_int_norm, delta_frets = global_utilities.frets_int_normalize(frets_int)
    return (is_movable_form, frets_int_norm, delta_frets)


def interval_to_hstep(interv):
    '''
    turn a string interval to half-step (semitones distance)
    ie: 'b5' -> 6, #11 -> 18
    
    interv: String, interval in string notation 
    
    return: Number, semitones distance (numeric interval between the two notes)
    '''
    # interv_names = [('R',), ('b2',), ('2',), ('b3',), ('3',), ('4',), ('b5', '#4'), ...
    for idx, elem in enumerate(global_constants.interv_names):
        if interv in elem:
            return idx
    return None


def hstep_to_interval(hstep):
    '''
    given an half number (semitones interval between the two notes)
    this function return the corresponding interval in string notation 
    ie: f(3) -> 'b3' or f(6) -> b5
    
    hstep: Number, half-step (semitones interval) number
    
    return: String, interval
    '''
    # interv_names = [('R',), ('b2',), ('2',), ('b3',), ('3',), ('4',), ('b5', '#4'), ...
    return global_constants.interv_names[hstep][0]


def hsteps_to_intervals(hsteps_lst):
    '''
    given an half-steps list of numbers (semitones interval between the two notes)
    this function return a list of these intervals in string notation 
    ie: f([None, 0, 3, 10, 2, 7]) -> [None, 'R', 'b3', 'b7', '2', '5']
    
    hsteps_lst: List, half-steps (semitones interval) number list
    
    return: List, string list of intervals
    '''
    act_interval = None
    intervals_lst = []
    for hstep in hsteps_lst:
        if hstep is not None:
            # interv_names = [('R',), ('b2',), ('2',), ('b3',), ('3',), ('4',), ('b5', '#4'), ..
            act_interval = global_constants.interv_names[hstep][0]
            intervals_lst.append(act_interval)
        else:
            intervals_lst.append(None)
    return intervals_lst


def intervals_to_hsteps(frml_interv):
    '''
    turn a string formula tuple to half-steps formula tuple
    ie: ('R','b3','5','7','9','11','13') -> (0,3,7,11,14,17,21)
    
    frml_interv: Tuple, chord interval formula
    
    return: Tuple, half-steps numeric formula tuple
    '''    
    hsteps = []   
    for elem in frml_interv:
        # get single semitones distance
        hstep = interval_to_hstep(elem)
        hsteps.append(hstep)
    return tuple(hsteps)


def reduce_hstep_to_first_octave(hstep):
    '''
    normalize semitone distance to first octave
    ie: 18 -> 6 (#11 is enharmonic to b5)
    
    hstep: Number, semitone distance
    
    return Number, semitone distance reduced to first ocatve (rhstep)
    '''    
    if hstep > 11:
        # mod division: get the remainder of a division problem.
        rhstep = (hstep % 12)
        return (hstep % 12)
    else:
        rhstep = hstep
    return rhstep


def intervals_to_rhsteps(frml_interv):
    '''
    Given a formula tuple get a of normalized and semitones distances tuple
    ie: ('R','b3','5','7','9','11','13') -> (0, 3, 7, 11, 2, 5, 9)
    
    frml_interv: Tuple, chord interval formula
    
    return: Tuple, half-steps normalized formula tuple (rhsteps)
    ''' 
    # ('R','b3','5','7','9','11','13') -> (0,3,7,11,14,17,21) = hsteps
    hsteps = intervals_to_hsteps(frml_interv)
    rhsteps = []
    for hstep in hsteps:
        # turn single hstep to first octave (normalized)
        rhstep = reduce_hstep_to_first_octave(hstep)
        rhsteps.append(rhstep)
    return tuple(rhsteps)


def intervals_to_sorted_rhsteps(frml_interv):
    '''
    Given a formula tuple get a of normalized and sorted semitones distances tuple
    ie: ('R','b3','5','7','9','11','13') -> (0, 2, 3, 5, 7, 9, 11)
    
    frml_interv: Tuple, chord interval formula
    
    return: Tuple, half-steps sorted and normalized formula tuple (rhsteps)
    ''' 
    # ('R','b3','5','7','9','11','13') -> intervals_to_rhsteps -> (0,3,7,11,14,17,21) = rhsteps
    # -> list() -> [0, 3, 7, 11, 14, 17, 21]
    rhsteps = list(intervals_to_rhsteps(frml_interv))
    # sort resulting list: [0, 3, 7, 11, 2, 5, 9] -> [0, 2, 3, 5, 7, 9, 11]
    rhsteps.sort()
    return tuple(rhsteps)


def hstep_to_note(root_note, hstep, flsh):
    '''
    Given a root note, a number of semitones (half-steps, hsteps) and a 'flat'/'sharp' type, 
    return the note corresponding to that interval from root note in 'flat'/'sharp' style
    ie: hstep_to_note('F#', 7, 'sharp') -> 'C#'
        hstep_to_note('F#', 7, 'flat')  -> 'Db'
    
    root_note: String, root_note name
    hstep: number of semitones (hsteps) from root
    flsh: String, 'flat'/'sharp' style of output note
    
    return String note corresponding to root note + hsteps in 'flat'/'sharp' style
    '''
    root_note_2octaves = n_octaves(root_note, 2, flsh)
    return root_note_2octaves[hstep]


def notes_to_hstep(root_note, second_note):
    '''
    Given a root note and a second note, return
    the number of semitones (half-steps, hsteps) between the two notes
    ie: notes_to_hstep('F#', 'C#') -> 7
    
    root_note, second_note: String, root_and second note name
    
    return Number, half-steps corresponding to the interval between the two notes
    '''
    root_note = normalize_note_name(root_note)
    # check if root_note is in latin notation then convert it to english notation
    if is_latin_note(root_note): root_note = conv_note_latin2en(root_note)
    second_note = normalize_note_name(second_note)
    # check if second_note is in latin notation then convert it to english notation
    if is_latin_note(second_note): second_note = conv_note_latin2en(second_note)
    # F# -> 'sharp'
    flsh_type_for_root_note = isnote_flsh(root_note)
    # C# -> 'sharp'
    flsh_type_for_second_note = isnote_flsh(second_note)
    # if notes are two different kind, ie: F#, Db
    if flsh_type_for_root_note != flsh_type_for_second_note:
        # then Db -> C#
        second_note = flsh_note_convers(second_note)
    # 1 octave chromatic scale for root note
    # ['F#','G','G#','A','A#','B','C','C#','D','D#','E','F']
    root_note_octave = n_octaves(root_note, 1, flsh_type_for_root_note)
    second_note_index = root_note_octave.index(second_note)
    return second_note_index


def singl_fret_to_note(string, fret_int, flsh):
    '''
    Given number of 'guitar string', fret number on that string and flat/sharp
    style of the note to return we get what note is. 
    ie: singl_fret_to_note(6, 4, 'sharp'):  G#
        singl_fret_to_note(6, 4, 'flat'):   Ab
    
    string, Number, number of guitar string: low E is 6, high e is 1
    fret_int: Number, fret number
    flsh: String, 'flat'/'sharp' style of output note
    
    return: String, what note is on guitar neck
    '''    
    # string_base is guitar open note on that string: 6 is (low) 'E'
    # guitar_strings = ['E', 'A', 'D', 'G', 'B', 'E']
    string_base = global_constants.guitar_strings[(6 - string)]
    # what note we have on that fret
    guitar_note = hstep_to_note(string_base, fret_int, flsh)
    return guitar_note


def notes_validator(notes):
    '''
    given a string note list, representing notes in a chord, this function output all valid 
    notes that can be present in another chord extending the original one (like a slash chord). 
    This is because in a chord if a natural note is half step close to an accidental note that has an 
    enharmonic equivalent then it must not have the same name. For example G is a natural note 
    and a chord tone then half step up/down we have Gb and G# which have enharmonic equivalent in F# and Ab. 
    So if another chord note is G# then we know that we must use Ab not G#. Of course natural notes 
    do not have enharmonic equivalents so they cannot be replaced.
    ie: notes_validator([None,D,A,D,F#,A]). Now we must build a valid slashes list. 
    We start by considering all notes: 
    [C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B]
    
    D, A and F# are chord tones so they must be present. Now D has Db and D# close an half step,
    same name and they have enharmonic equivalent in C# and Eb. So we forbid Db and D#. Same for A,
    we forbid Ab and A# and allow G# and Bb. For F# we have only F close an half step with same name.
    We cannot forbid F for it's a natural note with no enharmonic equivalent. Note that the case
    we have both F and F# never happens because we first check natural notes in the function.
    So at at lat we omit
    only Db, D#, Ab, A#, ie: [C, C#, D, Eb, E, F, F#, Gb, G, G#, A, Bb, B]
    
    notes: List of strings, input notes
    
    return List, valid chord note list  
    '''
    # notes = [None, 'G#', 'C', 'F#', 'G#', None]
    
    # enharm_dict is a dict with natural notes as keys (not replacable) and flat/sharp notes
    # as values that are half step close and have an enharmonic equivalent
    enharm_dict = {
          'C': ['C#']
        , 'D': ['Db', 'D#']
        , 'E': ['Eb']
        , 'F': ['F#']
        , 'G': ['Gb', 'G#']
        , 'A': ['Ab', 'A#']
        , 'B': ['Bb']
        }    
    
    for note in notes:
        for k, v in list(enharm_dict.items()):
            # 'C' == 'C'
            # natural notes
            if note == k:
                # erase the values of flat/sharp
                # 'C': ['C#'] -> 'C': []
                enharm_dict[note] = []
            # if a note is flat/sharp with two elem (G#) in enharm_dict:
            # erase the other element
            # 'G': ['Gb', 'G#'] -> 'G': ['G#']
            # if a note is flat/sharp with one elem (F#) in enharm_dict:
            # do nothing beacuse F# is chord tone and F is natural note
            if note in v:
                if (len(v) > 1):
                    # 'G': ['G#']
                    if v[0] == note: enharm_dict[k] = [v[0]]
                    if v[1] == note: enharm_dict[k] = [v[1]]
    
    # enharm_dict = {
    #       'C': []
    #     , 'D': ['Db', 'D#']
    #     , 'E': ['Eb']
    #     , 'F': ['F#']
    #     , 'G': ['G#']
    #     , 'A': ['Ab', 'A#']
    #     , 'B': ['Bb']
    #     } 
    valid_notes = []
    for k, v in list(enharm_dict.items()):
        valid_notes.append(k)
        if v:
            valid_notes = valid_notes + v
    # valid_notes = 
    # ['C','D','Db','D#','E','Eb','F','F#','G','G#','A','Ab','A#','B','Bb']
    return valid_notes


def frets_to_notes(frets, flsh):
    '''
    given a number frets list and a flat/sharp type return a note string list in 'flat'/'sharp' style
    ie: frets_to_notes([None, 3, 5, 5, 4, 3], 'flat') ->  [None, 'C', 'G', 'C', 'Eb', 'G']
        frets_to_notes([None, 3, 5, 5, 4, 3], 'sharp') -> [None, 'C', 'G', 'C', 'D#', 'G']
    
    frets: List, numbers fret list of a chord
    flsh: String, 'flat'/'sharp' style of output notes
    
    return: List, string note list in 'flat'/'sharp' style
    '''
    notes = []
    # enumerate(frets) -> (None, 0) (3, 1) (5, 2) (5, 3) (4, 4) (3, 5)
    # is a list of [((string - 6), fret) .. ]
    for string, fret in enumerate(frets):
        if fret is not None:
            act_note = singl_fret_to_note((6 - string), fret, flsh)
            notes.append(act_note)
        else:
            notes.append(None)
    return notes


def frets_to_valid_notes(frets, flsh):
    '''
    given a number frets list and a flat/sharp type return a note string list in 'flat'/'sharp' style
    as the frets_to_notes() function above but with correct enharmonic equivalent substitutions  
    following the half step rule of notes_validator() function
    ie: 
    frets_to_notes([3, 5, 4, 3, None, None], 'flat')       -> ['G', 'D', 'Gb', 'Bb', None, None]
    frets_to_valid_notes([3, 5, 4, 3, None, None], 'flat') -> ['G', 'D', 'F#', 'Bb', None, None]
    
    frets: List, numbers fret list of a chord
    flsh: String, 'flat'/'sharp' style of output notes
    
    return: List, string note list in 'flat'/'sharp' style
    '''
    notes = frets_to_notes(frets, flsh)
    valid_notes = notes_validator(notes)
    for index, note in enumerate(notes):
        if note and (note not in valid_notes):
            notes[index] = flsh_note_convers(note)
    return notes


def frets_to_hsteps(root_note, frets):
    '''
    given a root_note and a fret list return an half-steps list relative to root note (spanning 1 octave)
    ie: f('B', [None, 2, 0, 2, 2, 2]) -> [None, 'B', 'D', 'A', 'C#', 'F#'] -> [None, 0, 3, 10, 2, 7]
    
    root_note: String, root note name
    frets: List, number fret list of a chord
    
    return: List, half-steps normalized list
    '''
    hsteps_lst = []
    # B -> 'sharp'
    flsh_type_for_note = isnote_flsh(root_note)
    # ([None, 2, 0, 2, 2, 2], 'sharp') -> [None, 'B', 'D', 'A', 'C#', 'F#']
    fret_notes = frets_to_notes(frets, flsh_type_for_note)
    for elem in fret_notes:
        if elem is not None:
            # 'C#' -> 10
            act_hstep = notes_to_hstep(root_note, elem)
            hsteps_lst.append(act_hstep)
        else:
            hsteps_lst.append(None)
    return hsteps_lst


def frets_to_intervals(root_note, frets):
    '''
    given a root_note and a fret list return an interval list relative to root note
    ie: f('A', [5, 4, 0, 0, 5, 5]) -> ['R', '3', '4', 'b7', '5', 'R']
    
    root_note: String, root note name
    frets: List, number fret list of a chord
    
    return: List, string list of intervals
    '''
       
    # frets = [5, 4, 0, 0, 5, 5] -> hsteps = [0, 4, 5, 10, 7, 0]  (normalized 1 octave)
    hsteps = frets_to_hsteps(root_note, frets)
    # hsteps = [0, 4, 5, 10, 7, 0] -> intervals = ['R', '3', '4', 'b7', '5', 'R']
    intervals = hsteps_to_intervals(hsteps)
    # grouping, intervals_set = {'R', '3', '4', 'b7', '5'}
    intervals_set = set([elem for elem in intervals if elem])
    
    third_is_present = ('3' in intervals) or ('b3' in intervals)
    seventh_is_present = ('7' in intervals) or ('b7' in intervals)
    
    # special cases that break general rules
    # order of 'ifs' is important (from bigger to lower)
    # otherwis issubset does not work
    
    # 13sus4 -> R, 4, 5, b7, (9), 13
    if set(('R', '4', '6', 'b7')).issubset(intervals_set) and not third_is_present:
        intervals = modify_intervals_lst(intervals, '2', '9')
        intervals = modify_intervals_lst(intervals, '6', '13')    
    
    # maj9sus4 -> R, 4, 5, 7, 9
    elif set(('R', '2', '4', '7')).issubset(intervals_set) and not third_is_present:
        intervals = modify_intervals_lst(intervals, '2', '9')
    
    # 9sus4 -> R, 4, 5, b7, 9
    elif set(('R', '2', '4', 'b7')).issubset(intervals_set) and not third_is_present:
        intervals = modify_intervals_lst(intervals, '2', '9')
    
    # 13sus2 -> R, 2, 5, b7, 13
    elif set(('R', '2', '6', 'b7')).issubset(intervals_set) and not third_is_present:
        intervals = modify_intervals_lst(intervals, '6', '13')    

    else:
        
        # general rules
        
        # sus chords
        if third_is_present:
            if '2' in intervals: intervals = modify_intervals_lst(intervals, '2', '9')
            if 'b2' in intervals: intervals = modify_intervals_lst(intervals, 'b2', 'b9')
            if '4' in intervals: intervals = modify_intervals_lst(intervals, '4', '11')
            
        # dominant7 and min7 chords
        if seventh_is_present and third_is_present:
            if '2' in intervals: intervals = modify_intervals_lst(intervals, '2', '9')
            if '4' in intervals: intervals = modify_intervals_lst(intervals, '4', '11')
            if '6' in intervals: intervals = modify_intervals_lst(intervals, '6', '13')
        
        # dim7 chords
        if ('b3' in intervals) and ('b5' in intervals):
            if '6' in intervals: intervals = modify_intervals_lst(intervals, '6', 'bb7')
        
        # cannot exist 3 and b3 intervals    
        if '3' in intervals:
            if 'b3' in intervals: intervals = modify_intervals_lst(intervals, 'b3', '#9')    
        # cannot exist 5 and b5 intervals
        if '5' in intervals:
            if 'b5' in intervals: intervals = modify_intervals_lst(intervals, 'b5', '#11')
            if '#5' in intervals:
                if seventh_is_present: intervals = modify_intervals_lst(intervals, '#5', 'b13')
                else: intervals = modify_intervals_lst(intervals, '#5', 'b6')
    
    return intervals


def modify_intervals_lst(intervals, old_interval, new_interval):
    '''
    given an intervals list and 2 interval as strings (old and new)
    this function return the original list with old interval replaced by new interval
    ie: f(['R', '3', '4', 'b7', '5', 'R'], '4', '11') -> ['R', '3', '11', 'b7', '5', 'R']
    
    intervals: List, intervals string list
    old_interval: interval to be searched in intervals list
    new_interval: interval to be replaced in intervals list
    
    return: List, modified (serch/replace) intervals list
    '''
    final_list = []
    for elem in intervals:
        if elem is not None:
            if (elem != old_interval):
                final_list.append(elem)
            else:
                final_list.append(new_interval)
        else:
            final_list.append(None)
    return final_list


def modify_hsteps_lst(hsteps_lst, old_hstep, new_hstep):
    '''
    given an half-steps list and 2 half-steps numbers (old and new)
    this function return the original list with old hstep replaced by new hstep
    ie: f([None, 0, 3, 10, 2, 7], 2, 14) -> [None, 0, 3, 10, 14, 7]
    
    hsteps_lst: List, half-steps list
    old_hstep: half-steps to be searched in half-steps list
    new_hstep: half-steps to be replaced in half-steps list
    
    return: List, modified (serch/replace) half-steps list
    '''
    final_list = []
    for elem in hsteps_lst:
        if elem is not None:
            if (elem != old_hstep):
                final_list.append(elem)
            else:
                final_list.append(new_hstep)
        else:
            final_list.append(None)
    return final_list


def grpsort_hsteps_lst(hsteps_lst):
    '''
    given an half-steps list this function return the original list 
    with half steps grouped (remove duplicates and None elements) and sorted
    ie: f([0, 4, 10, 2, 4, None]) -> [0, 2, 4, 10]
    
    hsteps_lst: List, half-steps list
    
    return: List, grouped (removed None elements) and sorted half-steps list
    '''
    # remove None from hsteps_lst
    # [0, 4, 10, 2, 4, None] -> [0, 4, 10, 2, 4]
    hsteps_fltr_lst = [elem for elem in hsteps_lst if elem is not None]
    # group by changing into a set -> (0, 4, 10, 2)
    hsteps_grp_set = set(hsteps_fltr_lst)
    # turn into a list for sorting -> [0, 4, 10, 2]
    hsteps_grpsort_lst = list(hsteps_grp_set)
    # sort -> [0, 2, 4, 10]
    hsteps_grpsort_lst.sort()
    return hsteps_grpsort_lst


def autocomplete_chord(chord_name, frets_slst, fingers_slst=None, intervals_slst=None):
    '''
    given at least a chord name and a fret string list, this function try to guess
    fingers list (as strings) and interval list (as strings) using
    autofingers.chord_autofingers() and global_utilities.crd_slst2ilst()
    
    ie:
        autocomplete_chord(C7, ['x', '3', '2', '3', '1', '0']) ->
        (
              'C7'
            , ['x', '3', '2', '3', '1', '0']
            , ['x', '3', '2', '4', '1', 'x']
            , [None, 'R', '3', 'b7', 'R', '3']
        )
        
    if optional agrument fingers_slst is given fingers are not guessed 
    and original fingers_slst is returned
    
    if optional agrument intervals_slst is given intervals are not guessed 
    and original intervals_slst is returned
    
    chord_name: String, chord name
    frets_slst: List, fret list of the chord as strings
    fingers_slst: List, finger list of the chord as strings, optional param
    intervals_slst: List, interval list of the chord as strings, optional param
    
    return: Tuple: (chord_name, frets_slst, guessed fingers_slst, guessed intervals_slst)
    '''
    # parse_chord_name(F#m(no5)/Gb) -> ('F#', 'm', '(no5)', 'Gb')
    parsed_chord_name = chord_parser.parse_chord_name(chord_name)
    root_note = parsed_chord_name[0]
    if not fingers_slst:
        fingers_slst = autofingers.chord_autofingers(frets_slst)
    if not intervals_slst:
        frets_lst = global_utilities.crd_slst2ilst(frets_slst)
        intervals_slst = frets_to_intervals(root_note, frets_lst)
    return (chord_name, frets_slst, fingers_slst, intervals_slst)



if __name__ == "__main__":
    
    # testing this functions
    
    print('------------------  testing  ------------------')
    
    test_note1 = 'f#'
    test_note2 = 'SOLb'    
    test_note3 = 'C#'
    test_note4 = 'Cm7/G#'
    test_minmaj = 'major'
    test_flsh = 'sharp'
    
    print('\n- isnote_flsh(' + conv_note_latin2en(test_note2) + '):', \
        isnote_flsh(conv_note_latin2en(test_note2)))    

    print('\n- is_latin_note(' + test_note2 + '):', is_latin_note(test_note2))

    print('\n- conv_note_latin2en(' + test_note2 + '):', conv_note_latin2en(test_note2))
    
    print('\n- conv_note_en2latin(' + test_note3 + '):', conv_note_en2latin(test_note3))
    
    print('\n- conv_chordname_en2latin(' + test_note4 + '):', conv_chordname_en2latin(test_note4))

    print('\n- normalize_note_name(' + test_note1.lower() + '):', normalize_note_name(test_note1.lower()))
    
    print('\n- flsh_note_convers(' + test_note1 + '):', flsh_note_convers(test_note1))    

    print('\n- music_circle_flsh(' + test_note3 + ', ' + test_minmaj + '):', \
        music_circle_flsh(test_note3, test_minmaj))
    
    print('\n- n_octaves(' + test_note1 + ', 1, ' + test_flsh + '):', \
        n_octaves(test_note1, 1, test_flsh))
    
    print('\n- swap_flat_sharp(' + test_flsh + '):', swap_flat_sharp(test_flsh))
    
    print('\n- reverse_interv(''#5''):', reverse_interv('#5'))
    
    print('\n- reverse_interv(''6''):', reverse_interv('6'))
    
    print('\n- quality_to_majmin(''mb6(Add11)''):', quality_to_majmin('mb6(Add11)'))

    test_latin_names = [
          'LAadd9/MI', 'LA/DO#', 'LA/SOL#', 'SOLb/REb'
        , 'LAm/FA#', 'SI11/LA', 'B7/F#', 'SI/RE#'
        , 'D7(no5)/Bb', 'RE7(no5)/SIb'
        ]
    
    print('\nTesting is_latin_chord\n----------------------')
    for crd in test_latin_names:
        print('* ', crd, ' -> ', is_latin_chord(crd))

    print('\n- lowest_root_in_chord(''Dbmaj7'', [None, 4, 6, 5, 6, 0]):', \
        lowest_root_in_chord('Dbmaj7', [None, 4, 6, 5, 6, 4]))

    print('\n- lowest_root_in_chord(''Bb'', [None, 1, 3, 3, 3, 1]):', \
        lowest_root_in_chord('Bb', [None, 1, 3, 3, 3, 1]))

    print('\n- Dbmaj7 -> chord_normalize([''x'',''4'',''6'',''5'',''6'',''4'']):\n\t', \
        chord_normalize(['x', '4', '6', '5', '6', '4']))

    print('\n- interval_to_hstep(''b5''):', interval_to_hstep('b5'))
    
    print('\n- hstep_to_interval(''6''):', hstep_to_interval(6))
    
    formula = ('R', 'b3', '5', '7', '9', '11', '13')
    hsteps = intervals_to_hsteps(formula)    
    
    print('\n- hsteps_to_intervals(' + str(hsteps) + '):', hsteps_to_intervals(hsteps))
    
    print('\n- intervals_to_hsteps(' + str(formula) + '):', intervals_to_hsteps(formula))    
    
    print('\n- reduce_hstep_to_first_octave(18):', reduce_hstep_to_first_octave(18))

    print('\n- intervals_to_rhsteps(' + str(formula) + '):', intervals_to_rhsteps(formula))
    
    print('\n- intervals_to_sorted_rhsteps(' + str(formula) + '):', intervals_to_sorted_rhsteps(formula))
    
    print('\n- hstep_to_note(' + test_note1 + ', 7, ' + test_flsh + '):', \
        hstep_to_note(test_note1, 7, test_flsh))
    
    # print hstep_to_note('F#', 7, 'flat')
    
    print('\n- notes_to_hstep(' + test_note1 + ', ' + test_note3 + '):', \
        notes_to_hstep(test_note1, test_note3))
    
    print('\n- singl_fret_to_note(6, 4, sharp):', singl_fret_to_note(6, 4, 'sharp'))
    
    print('\n- notes_validator([None, D, A, D, F#, A]):\n\t', \
        notes_validator([None,'D','A','D','F#','A']))

    print('\n- notes_validator(None, G#, C, F#, G#, None):\n\t', \
        notes_validator([None, 'G#', 'C', 'F#', 'G#', None]))    

    test_chord0 = [' 5', '4', '0', '0', '5 ', '5']

    test_chord1 = ('LA11', 'LA', global_utilities.crd_slst2ilst(test_chord0))   
    print('\n- frets_to_notes(' + str(test_chord1[2]) + ', ''sharp''):\n\t', \
        frets_to_notes(test_chord1[2], 'sharp'))

    print('\n- frets_to_notes([3, 5, 4, 3, None, None], ''flat''):\n\t', \
        frets_to_notes([3, 5, 4, 3, None, None], 'flat'))

    print('\n- frets_to_valid_notes([3, 5, 4, 3, None, None], ''flat''):\n\t', \
        frets_to_valid_notes([3, 5, 4, 3, None, None], 'flat'))

    hsteps_lst = frets_to_hsteps(test_chord1[1], test_chord1[2])
    print('\n- frets_to_hsteps(' + str(test_chord1[1]) + ', ' + str(test_chord1[2]) + '):\n\t', \
        hsteps_lst)  
    
    print('\n- modify_intervals_lst(["R", "3", "4", "b7", "5", "R"], "4", "11"):\n\t', \
        modify_intervals_lst(['R', '3', '4', 'b7', '5', 'R'], '4', '11'))    

    print('\n- frets_to_intervals(' + str(test_chord1[1]) + ', ' + str(test_chord1[2]) + '):\n\t', \
        frets_to_intervals(test_chord1[1], test_chord1[2]))
    
    print('\n- modify_hsteps_lst(' + str(hsteps_lst) + ', 4, 16):\n\t', \
        modify_hsteps_lst(hsteps_lst, 4, 16))   

    hsteps_grpsort_lst = grpsort_hsteps_lst(hsteps_lst)
    
    print('\n- grpsort_hsteps_lst(' + str(hsteps_lst) + '):\n\t', \
        hsteps_grpsort_lst)

    test_chord = 'C7'
    test_fret_slist = ['x', '3', '2', '3', '1', '0']
    dummy_fingers = ['Y', '4', '2', 'Y', '1', 'y']
    dummy_intervals = [None, 'b', 'Z', 'K', '8', '2']
    
    print('\n- autocomplete_chord(' + test_chord + \
          ', ' + str(test_fret_slist) + \
          '):\n   ', autocomplete_chord(test_chord, test_fret_slist))

    print('\n- autocomplete_chord(' + test_chord + \
          ', ' + str(test_fret_slist) + ', ' + str(dummy_fingers) + \
          '):\n   ', autocomplete_chord(test_chord, test_fret_slist, dummy_fingers))

    print('\n- autocomplete_chord(' + test_chord + \
          ', ' + str(test_fret_slist) + ', ' + str(dummy_fingers) + ', ' + str(dummy_intervals) + \
          '):\n   ', autocomplete_chord(test_chord, test_fret_slist, dummy_fingers, dummy_intervals))
