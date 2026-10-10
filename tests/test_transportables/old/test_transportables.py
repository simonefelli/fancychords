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
from libs import transportables


if __name__ == "__main__":
    
    # copy paste from ods file
    trasp_chords_str_lst = (
          'C7    x,3,2,3,1,0    x,3,2,4,1,x'
        , 'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x'
        , 'Fmaj7    1,x,2,2,1,x    1,x,3,4,2,x'
        ,
        )
    
    trasp_chords_lst = []
    
    print('##########################################################################\n')
    print('Input Chords:\n-------------')
    
    for trasp_chords_str in trasp_chords_str_lst:
        '''
        turn input 'trasp_chords_str_lst'
        (
          'C7    x,3,2,3,1,0    x,3,2,4,1,x'
        , 'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x'
        ,
        )
        
        into
        
        [
          ['C7',    [None, 3, 2, 3, 1, 0],    ['x', '3', '2', '4', '1', 'x'], 5, 'major']
        , ['Dm7b5', [None, 5, 6, 5, 6, None], ['x', '1', '3', '2', '4', 'x'], 5, 'minor']

        ]
        '''
        # 'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x' -> ['Dm7b5', 'x,5,6,5,6,x', 'x,1,3,2,4,x']
        chord_name,  frets_int_str, fingers_str_str = trasp_chords_str.split('    ')
        # 'x,5,6,5,6,x' > [None, 5, 6, 5, 6, None]
        frets_int_lst = global_utilities.crd_slst2ilst(frets_int_str.split(','))
        # 'x,1,3,2,4,x' -> ['x', '1', '3', '2', '4', 'x']
        fingers_str_lst = global_utilities.crd_str2slst(fingers_str_str)
        # ('D', 5, 'minor') = find_rootstring_majmin('Dm7b5', [None, 5, 6, 5, 6, None])
        root_note, root_string, majmin = transportables.find_rootstring_majmin(chord_name, frets_int_lst)
        '''
        trasp_chords_lst = [
              ['C7',    [None, 3, 2, 3, 1, 0],    ['x', '3', '2', '4', '1', 'x'], 5, 'major']
            , ['Dm7b5', [None, 5, 6, 5, 6, None], ['x', '1', '3', '2', '4', 'x'], 5, 'minor']
            ]
        '''
        trasp_chords_lst.append([chord_name, frets_int_lst, fingers_str_lst, root_string, majmin])
        print(
              '> '
            , '{:<11}'.format(chord_name)
            , '{:<35}'.format(str(frets_int_lst))
            , '{:<35}'.format(str(fingers_str_lst))
            , '{:<7}'.format(str(root_string))
            , majmin
            )
    
    print('\n##########################################################################')
    
    is_first_print = True
    for trasp_chord in trasp_chords_lst:
        '''
        chord_list = [
          ('C7',  [None, 3, 2, 3, 1, None], ['x', '3', '2', '4', '1', 'x'], [None, 'R', '3', 'b7', 'R', None], None)
        , ('C#7', [None, 4, 3, 4, 2, None], ['x', '3', '2', '4', '1', 'x'], [None, 'R', '3', 'b7', 'R', None], 'Db7')
        , ('D7',  [None, 5, 4, 5, 3, None], ['x', '3', '2', '4', '1', 'x'], [None, 'R', '3', 'b7', 'R', None], None)
        , ....
        ]
        '''
        chord_list = transportables.transport(trasp_chord)
        for chord in chord_list:
            if not is_first_print:
                print('\n===================================')
            is_first_print = False              
            chord_name = chord[0]
            chord_name_enharm = chord[4]
            # chord_parser.parse_chord_name('C7') -> ('C', '7', '', '')
            root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord_name)
            # global_constants.quality_family['7'] > 'Dominant'
            family = global_constants.quality_family[quality]
            latin_root_note = music_utilities.conv_note_en2latin(root_note)
            latin_chord_name = music_utilities.conv_chordname_en2latin(chord_name)
            # [None, 3, 2, 3, 1, None] -> 'x,3,2,3,1,x'
            frets_str = ','.join(global_utilities.crd_ilst2slst(chord[1]))
            # ['x', '3', '2', '4', '1', 'x'] -> 'x,3,2,4,1,x'
            fingers_str = ','.join(global_utilities.crd_ilst2slst(chord[2]))
            print('\n* Txt Latin Output')
            print(
                latin_chord_name + '\t' + frets_str + '\t' + fingers_str + '\t%\t%\t%\t' + \
                latin_root_note + '/' + family
                )
            print('\n* Ods Output')
            print(
                root_note + '\t' + family + '\t' + quality + '\t' + detail + \
                 '\t' + global_utilities.chain(slash_note, '/', '\t') + \
                 '\t' + global_utilities.lst2str(chord[1], '\t', 'x') + \
                 '\t' + global_utilities.lst2str(chord[2], '\t', 'x')
                )
            if chord_name_enharm:
                root_note_enharm, quality_enharm, detail_enharm, slash_note_enharm = chord_parser.parse_chord_name(chord_name_enharm)
                latin_root_note_enharm = music_utilities.conv_note_en2latin(root_note_enharm)
                latin_chord_name_enharm = music_utilities.conv_chordname_en2latin(chord_name_enharm)
                print('\n* Txt Latin Enharm Output')
                print(
                    latin_chord_name_enharm + '\t' + frets_str + '\t' + fingers_str + '\t%\t%\t%\t' + \
                    latin_root_note_enharm + '/' + family
                    )
                print('\n* Ods Enharm Output')
                print(
                    root_note_enharm + '\t' + family + '\t' + quality_enharm + '\t' + detail_enharm + '\t' + slash_note_enharm + '\t' + \
                    global_utilities.lst2str(chord[1], '\t', 'x') + '\t' + \
                    global_utilities.lst2str(chord[2], '\t', 'x')
                    )
            
        print('\n##########################################################################')
