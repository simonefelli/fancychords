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

from libs import global_constants
from libs import global_utilities
from libs import music_utilities
from libs import chord_parser
from libs import intervals


def find_rootstring_majmin(chord_name, frets_int):
    '''
    From a chord_name and frets_int list get:
    - chord root_note
    - lowest root guitar string
    - 'major'/'minor' nature of chord
    ie: From ('A7/F#', [2, None, 2, 2, 2, 3]    ) -> ('A', 3, major)
        From ('Bdim7', [None, 2, 3, 1, 3, None])) -> ('B', 5, minor)
    
    chord_name: String, name of the chord
    frets_int: List of numbers, fret numbers of a chord
    
    return a tuple: (
        - root_note: String, root_note
        - root_string: Number, guitar string of root note (6th is lowest E)
        - majmin: String, 'major'/'minor' nature of chord
    )
    '''
    root_note = chord_parser.parse_chord_name(chord_name)[0]
    root_string = music_utilities.lowest_root_in_chord(chord_name, frets_int)
    majmin = intervals.chord_finder(root_note, frets_int)[0][7]
    return (root_note, root_string, majmin)


def transport(trasp_chord):
    '''
    From a chord, scale it up till 12 chord
    ie: From C get C# / D / D# ...
    
    trasp_chord: Tuple, (chord_name, frets_int, fingers, root_string, majmin)
    - chord_name: String, name of the chord
    - frets_int: List of numbers, fret numbers of a chord
    - fingers: List of strings, finger list of a chord
    - root_string: Number, guitar string of root note (6th is lowest E)
    - majmin: String, 'major'/'minor' nature of chord
    
    enharmonic: Boolean, if True output also enharmonic scaled chords 
        ie: C -> C#, Db / D / D#, Eb/ ...
    
    return: Text output and List of scaled chord list
    
    scaled chord list is in the form of
    [
      (chord_name, frets_int_list, fingers_list, intervals_list, enharmonic)
    , ...
    ] 
    
    where enharmonic is chord enharmonic name (Null if chord name stays the same)
    
    ie:
    [    
      ('Fdim7',  [None, 2, 3, 1, 3, None], ['x', '2', '3', '1', '4', 'x'], [None, 'b5', 'R', 'b3', 'bb7', None], None)
    , ('Gbdim7', [None, 3, 4, 2, 4, None], ['x', '2', '3', '1', '4', 'x'], [None, 'b5', 'R', 'b3', 'bb7', None], 'F#dim7')
    , ...
    ] 
    '''

    # final_list = [(new_chord_name, new_frets_int, fingers, intervals), ...]
    final_list = []
    
    # get chord infos
    #  ('Cm7/G', [3, 3, 5, 3, 4, 3], [1, 1, 3, 1, 2, 1], 5, 'minor')
    (chord_name, frets_int, fingers, root_string, majmin) = trasp_chord
    # get chord name infos, parse_chord_name(chord_name) ->
    # root_note = 'C', quality = 'm7', detail = '', slash_note = 'G'
    root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord_name)
    # chord is flat or sharp throughout music circle based on root_note, majmin
    # flsh_root = 'flat'
    flsh_root = music_utilities.music_circle_flsh(root_note, majmin)
    # root_fret = 3
    root_fret = frets_int[6 - root_string]
    delta_step = 0
    # at most go up till 12 fret
    while (root_fret + delta_step) <= 12:
        # scale root note by delta_step
        # example: if delta_step == 1 -> new_root_note = 'Db'
        new_root_note = music_utilities.singl_fret_to_note(root_string, root_fret + delta_step, flsh_root)
        # scale frets_int by delta_step
        # new_frets_int =  [4, 4, 6, 4, 5, 4]
        new_frets_int = [fret + delta_step if fret else None for fret in frets_int]
        # interv =  ['5', 'R', '5', 'b7', 'b3', '5']
        interv = music_utilities.frets_to_intervals(new_root_note, new_frets_int)
        
        # if a slash note in chord name
        if slash_note:
            # get scaled slash flat/sharp -> flsh_slash = 'flat'
            flsh_slash = music_utilities.music_circle_flsh(new_root_note, majmin)
            # get scaled slash note -> new_slash_note = 'Ab'
            new_slash_note = music_utilities.hstep_to_note(slash_note, delta_step, flsh_slash)
            # check for valid slash: get valid_slashes list
            # to do so first get the notes from new_frets_int and then
            # do the correct enharmonic substitutions with notes_validator()
            # valid_slashes = ['C', 'C#', 'D', 'Db', 'E', 'F', 'F#', 'G', 'Gb', 'G#', 'A', 'Ab', 'B']
            notes = music_utilities.frets_to_notes(new_frets_int, flsh_slash)
            valid_slashes = music_utilities.notes_validator(notes)
            if new_slash_note not in valid_slashes:
                # if not a valid slash then reverse flat <-> sharp
                reversed_slash_note = music_utilities.flsh_note_convers(new_slash_note)
                # if reversed_slash_note is valid then assign to new_slash_note
                if reversed_slash_note in valid_slashes:
                    new_slash_note = reversed_slash_note
            # fulldetail = detail + slash -> '/Ab'
            new_fulldetails = detail + '/' + new_slash_note
        else:
            new_slash_note = ''
            new_fulldetails = detail
        #  new_chord_name = Dbm7/Ab
        new_chord_name = new_root_note + quality + new_fulldetails
        #  new_chord = ('Dbm7/Ab', [4, 4, 6, 4, 5, 4], [1, 1, 3, 1, 2, 1], 
        #                ['5', 'R', '5', 'b7', 'b3', '5'])
        # get enharmonic root_note -> 'C#'
        root_note_enharm = music_utilities.flsh_note_convers(new_root_note)
        # if, for example, C# != Db ( not the case for natural notes)
        if root_note_enharm != new_root_note:
            # and if a slash is present ('Ab')
            if new_slash_note:
                # get enharmonic slash_note -> 'G#'
                slash_note_enharm = music_utilities.flsh_note_convers(new_slash_note)
                # get enharmonic fulldetail -> ' /G#'
                fulldetails_enharm = detail + '/' + slash_note_enharm
            else:
                slash_note_enharm = ''
                fulldetails_enharm = detail
            # chord_name_enharm = 'C#m7/G#'
            chord_name_enharm = root_note_enharm + quality + fulldetails_enharm
        else:
            chord_name_enharm = None

        new_chord = (new_chord_name, new_frets_int, fingers, interv, chord_name_enharm)
        # append scaled chord to final list
        final_list.append(new_chord)
        delta_step += 1

    return final_list


if __name__ == "__main__":
    
    # testing these functions

    # trasp_chord element is (chord_name, frets_int, fingers, root_string, majmin)
    trasp_chords_assert = (
        
          ('F',     [1, 3, 3, 2, 1, 1],       ['1', '3', '4', '2', '1', '1'], 6, 'major')  # E Form
        , ('F7',    [1, 3, 1, 2, 1, 1],       ['1', '3', '1', '2', '1', '1'], 6, 'major')  # E Form
        , ('Fm',    [1, 3, 3, 1, 1, 1],       ['1', '3', '4', '1', '1', '1'], 6, 'minor')  # E Form
        , ('Bb',    [None, 1, 3, 3, 3, 1],    ['x', '1', '2', '3', '4', '1'], 5, 'major')  # A Form
        , ('Bb7',   [None, 1, 3, 1, 3, 1],    ['x', '1', '2', '1', '4', '1'], 5, 'major')  # A Form
        , ('Bbm',   [None, 1, 3, 3, 2, 1],    ['x', '1', '3', '4', '2', '1'], 5, 'minor')  # A Form
        , ('Bbm7',  [None, 1, 3, 1, 2, 1],    ['x', '1', '3', '1', '2', '1'], 5, 'minor')  # A Form
        
        # , ('Fdim7', [None, 2, 3, 1, 3, None], ['x' ,'2' ,'3' ,'1' ,'4' ,'x'], 4, 'minor')
         , ('Cm7/G', [3, 3, 5, 3, 4, 3],       ['1', '1', '3', '1', '2', '1'], 5, 'minor')  # C form
        # , ('Eb/G',  [3, None, 1, 3, 4, None], ['2', 'x', '1', '3', '4', 'x'], 4, 'major')  # D Form
        # , ('Bdim7', [None, 2, 3, 1, 3, None], ['x', '2', '3', '1', '4', 'x'], 5, 'minor')  # Dim5thfret
        # , ('A7/F#', [2, None, 2, 2, 2, 3],    ['T', 'x', '2', '2', '2', '4'], 3, 'major')  # Test
        )
    
    print('#####################################')
    
    for trasp_chord in trasp_chords_assert:
        chord_name = trasp_chord[0]
        frets_int =  trasp_chord[1]
        root_note, root_string, majmin = find_rootstring_majmin(chord_name, frets_int)
        if (root_string == trasp_chord[3]) and (majmin == trasp_chord[4]):
            result = 'OK: '
        else:
            result = 'KO: '
        print(result, '\t', chord_name, '\t', frets_int, '\t', root_string, '\t', majmin)
    
    print('#####################################')
    
    for trasp_chord in trasp_chords_assert:
        chord_list = transport(trasp_chord)
        for chord in chord_list:
            chord_name = chord[0]
            chord_name_enharm = chord[4]
            root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord_name)
            family = global_constants.quality_family[quality]
            latin_root_note = music_utilities.conv_note_en2latin(root_note)
            latin_chord_name = music_utilities.conv_chordname_en2latin(chord_name)
            frets_str = ','.join(global_utilities.crd_ilst2slst(chord[1]))
            fingers_str = ','.join(global_utilities.crd_ilst2slst(chord[2]))
            print(
                latin_chord_name + '\t' + frets_str + '\t' + fingers_str + '\t%\t%\t%\t' + \
                latin_root_note + '/' + family
                )
            
            print(
                root_note + '\t' + family + '\t' + quality + '\t' + detail + '\t' + global_utilities.chain(slash_note, '/', '\t', '\t') + \
                global_utilities.lst2str(chord[1], '\t', 'x') + '\t' + \
                global_utilities.lst2str(chord[2], '\t', 'x')
                )
            
            if chord_name_enharm:
                root_note_enharm, quality_enharm, detail_enharm, slash_note_enharm = chord_parser.parse_chord_name(chord_name_enharm)
                latin_root_note_enharm = music_utilities.conv_note_en2latin(root_note_enharm)
                latin_chord_name_enharm = music_utilities.conv_chordname_en2latin(chord_name_enharm)
                print(
                    latin_chord_name_enharm + '\t' + frets_str + '\t' + fingers_str + '\t%\t%\t%\t' + \
                    latin_root_note_enharm + '/' + family
                    )
                print(
                    root_note_enharm + '\t' + family + '\t' + quality_enharm + '\t' + detail_enharm + '\t' + slash_note_enharm + '\t' + \
                    global_utilities.lst2str(chord[1], '\t', 'x') + '\t' + \
                    global_utilities.lst2str(chord[2], '\t', 'x')
                    )
    
    print('#####################################')

