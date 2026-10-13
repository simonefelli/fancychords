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
global_constants: constant values shared by the libs: note names (english
and latin), chromatic scales, circle of fifths, the sets of allowed chars
for fingers and intervals used to validate input chords, interval names,
chord formulas, scales library and CAGED shapes.
"""



# major notes list
notes_eng =   ['C',  'D',  'E',  'F',  'G',   'A',  'B' ]
notes_latin = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']


# guitar strings
guitar_strings = ['E', 'A', 'D', 'G', 'B', 'E']


# flat reference chromatic scale octave
flat_chrscale =  ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
# sharp reference chromatic scale octave
sharp_chrscale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# flat/sharp -> reference chromatic scale octave
flsh_chrscale = {
    'flat': flat_chrscale,
    'sharp': sharp_chrscale
    }


# for each root note tells if it's scale has flat or sharps
# depending on major/minor case

# note this is for major keys only
# {note : ('sharp'/'flat', number of accidentals), ... }
major_music_circle = {
    'C': ('sharp', 0),
    'G': ('sharp', 1),
    'D': ('sharp', 2),
    'A': ('sharp', 3),
    'E': ('sharp', 4),
    'B': ('sharp', 5),
    'F#': ('sharp', 6),
    'C#': ('sharp', 7),
    'G#': ('sharp', 8),
    'D#': ('sharp', 9),
    'A#': ('sharp', 10),
    'F': ('flat', 1),
    'Bb': ('flat', 2),
    'Eb': ('flat', 3),
    'Ab': ('flat', 4),
    'Db': ('flat', 5),
    'Gb': ('flat', 6),
    'Cb': ('flat', 7),
    'Fb': ('flat', 8)
    }
# note this is for minor keys only
# {note : ('sharp'/'flat', number of accidentals), ... }
minor_music_circle = {
    'A': ('flat', 0),
    'E': ('sharp', 1),
    'B': ('sharp', 2),
    'F#': ('sharp', 3),
    'C#': ('sharp', 4),
    'G#': ('sharp', 5),
    'D#': ('sharp', 6),
    'A#': ('sharp', 7),
    'E#': ('sharp', 8),
    'D': ('flat', 1),
    'G': ('flat', 2),
    'C': ('flat', 3),
    'F': ('flat', 4),
    'Bb': ('flat', 5),
    'Eb': ('flat', 6),
    'Ab': ('flat', 7),
    'Db': ('flat', 8),
    'Gb': ('flat', 9),
    'Cb': ('flat', 10)
    }


fingers_set_allowed_chars = {
    't', 'T', '1', '2', '3', '4', 'x', 'X'
    }


intervals_set_allowed_chars = {
       'r', 'R', 'b2', '2', 'b3', '3', '4', 'b5', '#4', '5'
    , '#5', 'b6', '6', 'bb7', 'b7', '7', 'R', 'b9', '9'
    , '#9', '10', '11', '#11', '12', 'b13', '13', 'x', 'X'
    # 'h' for hidden format
    ,  'rh', 'Rh', 'b2h', '2h', 'b3h', '3h', '4h', 'b5h', '#4h', '5h'
    , '#5h', 'b6h', '6h', 'bb7h', 'b7h', '7h', 'Rh', 'b9h', '9h'
    , '#9h', '10h', '11h', '#11h', '12h', 'b13h', '13h'
    }


# common intervals, position in list give half step distance from root
interv_names = [
      ('R',)
    , ('b2',)
    , ('2',)
    , ('b3',)
    , ('3',)
    , ('4',)
    , ('b5', '#4')
    , ('5',)
    , ('#5', 'b6')
    , ('6', 'bb7')
    , ('b7',)
    , ('7',)
    , ('R',)
    , ('b9',)
    , ('9',)
    , ('#9',)
    , ('10',)
    , ('11',)
    , ('#11',)
    , ('12',)
    , ('b13',)
    , ('13',)
    ]


# intervals equivalences
reverse_interv_dict = {
    'b3':  '#2',
    'b5':  '#4',
    'b6':  '#5',
    'b7':  '#6',
    'b10': '#9',
    'b12': '#11',
    'b13': '#12'
    }


# chord formulas, for intervals.chord_finder(). Note: formula order matters
formulas_list = (
      ('5', ('R', '5'), 'major')
    , ('5(#11)', ('R', '5', '#11'), 'major')
    , ('(b5)', ('R', '3', 'b5'), 'major')
    , ('6b5', ('R', '3', 'b5', '6'), 'major')
    , ('maj7b5', ('R', '3', 'b5', '7'), 'major')
    , ('major', ('R', '3', '5'), 'major')
    , ('6', ('R', '3', '(5)', '6'), 'major')
    , ('6/9', ('R', '3', '(5)', '6', '9'), 'major')
    , ('6/11', ('R', '3', '(5)', '6', '11'), 'major')
    , ('maj7', ('R', '3', '5', '7'), 'major')
    , ('maj9', ('R', '3', '5', '7', '9'), 'major')
    , ('maj11', ('R', '3', '5', '7', '(9)', '11'), 'major')
    , ('maj13', ('R', '3', '5', '7', '(9)', '(11)', '13'), 'major')
    , ('maj7(#11)', ('R', '3', '5', '7', '#11'), 'major')
    , ('maj7#5', ('R', '3', '#5', '7'), 'major')
    , ('maj9#5', ('R', '3', '#5', '7', '9'), 'major')
    , ('(add9)', ('R', '3', '5', '9'), 'major')
    , ('(add9add11)', ('R', '3', '5', '9', '11'), 'major')
    , ('(add11)', ('R', '3', '5', '11'), 'major')
    , ('sus2sus4', ('R', '2', '4', '5'), 'major')
    , ('sus2', ('R', '2', '5'), 'major')
    , ('6sus2', ('R', '2', '5', '6'), 'major')
    , ('7sus2', ('R', '2', '5', 'b7'), 'major')
    , ('13sus2', ('R', '2', '5', 'b7', '13'), 'major')
    , ('maj7sus2', ('R', '2', '5', '7'), 'major')
    , ('sus2(#11)', ('R', '2', '5', '#11'), 'major')
    , ('sus4', ('R', '4', '5'), 'major')
    , ('6sus4', ('R', '4', '5', '6'), 'major')
    , ('7sus4', ('R', '4', '5', 'b7'), 'major')
    , ('maj7sus4', ('R', '4', '5', '7'), 'major')
    , ('9sus4', ('R', '4', '(5)', 'b7', '9'), 'major')
    , ('13sus4', ('R', '4', '5', 'b7', '(9)', '13'), 'major')
    , ('maj9sus4', ('R', '4', '5', '7', '9'), 'major')
    , ('7sus4(b13)', ('R', '4', '5', 'b7', 'b13'), 'major')
    , ('sus4(#5)', ('R', '4', '#5'), 'major')
    , ('maj7sus4(#5)', ('R', '4', '#5', '7'), 'major')
    , ('7', ('R', '3', '(5)', 'b7'), 'major')
    , ('9', ('R', '3', '5', 'b7', '9'), 'major')
    , ('11', ('R', '3', '5', 'b7', '(9)', '11'), 'major')
    , ('13', ('R', '3', '5', 'b7', '(9)', '(11)', '13'), 'major')
    , ('7b5', ('R', '3', 'b5', 'b7'), 'major')
    , ('9b5', ('R', '3', 'b5', 'b7', '9'), 'major')
    , ('7(#9,b5)', ('R', '3', 'b5', 'b7', '#9'), 'major')
    , ('7b9', ('R', '3', '5', 'b7', 'b9'), 'major')
    , ('7#9', ('R', '3', '5', 'b7', '#9'), 'major')
    , ('7(#11)', ('R', '3', '5', 'b7', '#11'), 'major')
    , ('7(b13)', ('R', '3', '(5)', 'b7', 'b13'), 'major')
    , ('7#5', ('R', '3', '#5', 'b7'), 'major')
    , ('9#5', ('R', '3', '#5', 'b7', '9'), 'major')
    , ('+', ('R', '3', '#5'), 'major')
    , ('+(add9)', ('R', '3', '#5', '9'), 'major')
    , ('m(maj7)b5', ('R', 'b3', 'b5', '7'), 'minor')
    , ('m', ('R', 'b3', '5'), 'minor')
    , ('mb6', ('R', 'b3', '5', 'b6'), 'minor')
    , ('mb6(add11)', ('R', 'b3', '5', 'b6', '11'), 'minor')
    , ('m6', ('R', 'b3', '5', '6'), 'minor')
    , ('m6(add9)', ('R', 'b3', '5', '6', '9'), 'minor')
    , ('m7', ('R', 'b3', '5', 'b7'), 'minor')
    , ('m9', ('R', 'b3', '5', 'b7', '9'), 'minor')
    , ('m11', ('R', 'b3', '5', 'b7', '(9)', '11'), 'minor')
    , ('m13', ('R', 'b3', '5', 'b7', '(9)', '(11)', '13'), 'minor')
    , ('m7(b13)', ('R', 'b3', '5', 'b7', 'b13'), 'minor')
    , ('m(maj7)', ('R', 'b3', '5', '7'), 'minor')
    , ('m(maj9)', ('R', 'b3', '5', '7', '9'), 'minor')
    , ('m(maj11)', ('R', 'b3', '5', '7', '(9)', '11'), 'minor')
    , ('m(maj13)', ('R', 'b3', '5', '7', '(9)', '(11)', '13'), 'minor')
    , ('m(add9)', ('R', 'b3', '5', '9'), 'minor')
    , ('m(add11)', ('R', 'b3', '5', '11'), 'minor')
    , ('m7(#5)', ('R', 'b3', '#5', 'b7'), 'minor')
    , ('m(maj7)#5', ('R', 'b3', '#5', '7'), 'minor')
    , ('dim', ('R', 'b3', 'b5'), 'minor')
    , ('m7b5', ('R', 'b3', 'b5', 'b7'), 'minor')
    , ('dim7', ('R', 'b3', 'b5', 'bb7'), 'minor')
    , ('dim9', ('R', 'b3', 'b5', 'bb7', '9'), 'minor')
    )


# scales formulas for helper_functions.generate_scale()
scales_library = {
      'major': (('R', '2', '3', '4', '5', '6', '7'), 'major', 'Major Scale')
    , 'minor_natural': (('R', '2', 'b3', '4', '5', 'b6', 'b7'), 'minor', 'Minor Natural Scale')
    , 'minor_harmonic': (('R', '2', 'b3', '4', '5', 'b6', '7'), 'minor', 'Minor Harmonic Scale')
    , 'minor_melodic': (('R', '2', 'b3', '4', '5', '6', '7'), 'minor', 'Minor Melodic Scale')
    , 'major_pentatonic': (('R', '2', '3', '5', '6'), 'major', 'Major Pentatonic Scale')
    , 'minor_pentatonic': (('R', 'b3', '4', '5', 'b7'), 'minor', 'Minor Pentatonic Scale')
    , 'major_blues_scale': (('R','2','b3','3','5','6'), 'major', 'Major Blues Scale')
    , 'minor_blues_scale': (('R','b3','4','b5','5','b7'), 'minor', 'Minor Blues Scale')
    , 'ionian': (('R', '2', '3', '4', '5', '6', '7'), 'major', 'Ionian Mode')
    , 'dorian': (('R', '2', 'b3', '4', '5', '6', 'b7'), 'minor', 'Dorian Mode')
    , 'phrygian': (('R', 'b2', 'b3', '4', '5', 'b6', 'b7'), 'minor', 'Phrygian Mode')
    , 'lydian': (('R', '2', '3', '#4', '5', '6', '7'), 'major', 'Lydian Mode')
    , 'mixolydian': (('R', '2', '3', '4', '5', '6', 'b7'), 'major', 'Mixolydian Mode')
    , 'aeolian': (('R', '2', 'b3', '4', '5', 'b6', 'b7'), 'minor', 'Aeolian Mode')
    , 'locrian': (('R', 'b2', 'b3', '4', 'b5', 'b6', 'b7'), 'minor', 'Locrian Mode')
    , 'lydian_dominant': (('R', '2', '3', '#4', '5', '6', 'b7'), 'major', 'Lydian Dominant Mode')
    , 'major_arpeggios': (('R', '3', '5'), 'major', 'Major Arpeggios')
    , 'minor_arpeggios': (('R', 'b3', '5'), 'minor', 'Minor Arpeggios')
    , 'maj7_arpeggios': (('R', '3', '5', '7'), 'major', 'Major7 Arpeggios')
    , 'min7_arpeggios': (('R', 'b3', '5', 'b7'), 'minor', 'Minor7 Arpeggios')
    , 'dom7_arpeggios': (('R', '3', '5', 'b7'), 'major', 'Dominant7 Arpeggios')
    , 'min7b5_arpeggios': (('R', 'b3', 'b5', 'b7'), 'minor', 'Minor7b5 Arpeggios')
    , 'octaves': (('R',), 'major', 'Octaves')
    }


# Dict with infos on slicing complete neck scales into CAGED Forms
caged_dict = {
      'G': {
            'major': (
              ('E Form', 2,  5)
            , ('D Form', 4,  8)
            , ('C Form', 7,  10)
            , ('A Form', 9,  13)
            , ('G Form', 11, 15)
            )
          , 'min7_arpeggios': (
              ('E Form', 3,  6)
            , ('D Form', 5,  8)
            , ('C Form', 7,  11)
            , ('A Form', 10,  13)
            , ('G Form', 12, 15)
            )
        }
    , 'A': {
            'blues_scale': (
              ('G Form', 2,  6)
            , ('E Form', 5,  8)
            , ('D Form', 7,  11)
            , ('C Form', 9,  13)
            , ('A Form', 12, 16)
            )        
        }
}


quality_family = {
    '5': 'Power',
    '5(#11)': 'Power',
    '(b5)': 'Major',
    '6b5': 'Major',
    'maj7b5': 'Major',
    '': 'Major',
    '6': 'Major',
    '6/9': 'Major',
    '6/11': 'Major',
    'maj7': 'Major',
    'maj9': 'Major',
    'maj11': 'Major',
    'maj13': 'Major',
    'maj7(#11)': 'Major',
    'maj7#5': 'Major',
    'maj9#5': 'Major',
    '(add9)': 'Add',
    '(add9add11)': 'Add',
    '(add11)': 'Add',
    'sus2sus4': 'Sus',
    'sus2': 'Sus',
    '6sus2': 'Sus',
    '7sus2': 'Sus',
    '13sus2': 'Sus',
    'maj7sus2': 'Sus',
    'sus2(#11)': 'Sus',
    'sus4': 'Sus',
    '6sus4': 'Sus',
    '7sus4': 'Sus',
    'maj7sus4': 'Sus',
    '9sus4': 'Sus',
    '13sus4': 'Sus',
    'maj9sus4': 'Sus',
    '7sus4(b13)': 'Sus',
    'sus4(#5)': 'Sus',
    'maj7sus4(#5)': 'Sus',
    '7': 'Dominant',
    '9': 'Dominant',
    '11': 'Dominant',
    '13': 'Dominant',
    '7b5': 'Altered',
    '9b5': 'Altered',
    '7(#9,b5)': 'Altered',
    '7b9': 'Altered',
    '7#9': 'Altered',
    '7(#11)': 'Altered',
    '7(b13)': 'Altered',
    '7#5': 'Altered',
    '9#5': 'Altered',
    '+': 'Augmented',
    '+(add9)': 'Augmented',
    'm(maj7)b5': 'Minor',
    'm': 'Minor',
    'mb6': 'Minor',
    'mb6(add11)': 'Minor',
    'm6': 'Minor',
    'm6(add9)': 'Minor',
    'm7': 'Minor',
    'm9': 'Minor',
    'm11': 'Minor',
    'm13': 'Minor',
    'm7(b13)': 'Minor',
    'm(maj7)': 'Minor',
    'm(maj9)': 'Minor',
    'm(maj11)': 'Minor',
    'm(maj13)': 'Minor',
    'm(add9)': 'Minor',
    'm(add11)': 'Minor',
    'm7(#5)': 'Minor',
    'm(maj7)#5': 'Minor',
    'dim': 'Diminished',
    'm7b5': 'Diminished',
    'dim7': 'Diminished',
    'dim9': 'Diminished'
    }
