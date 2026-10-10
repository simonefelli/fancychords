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


# --------------- IMPORTS -------------------

# builtin libs
import re

# --- External Libs ---
from libs import global_constants
from libs import global_utilities
from libs import music_utilities
from libs import chord_parser
from libs import transportables


# -------------- CONSTANTS ------------------

DIVIDER_STR = '##########################################################################'
SEP = '==================================='


# -------------- FUNCTIONS ------------------

def split_columns(line: str):
    """
    Split a line into columns using at least 4 spaces as separator.
    Falls back to splitting on any sequence of whitespace if needed.
    
    'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x' -> ['Dm7b5', 'x,5,6,5,6,x', 'x,1,3,2,4,x']
    """
    cols = re.split(r'\s{4,}', line.strip())
    if len(cols) == 1:
        cols = re.split(r'\s+', line.strip())
    return cols


def parse_input_line(line: str):
    """
    Parse a single input line into (chord_name, frets_int_list, fingers_str_list).
    'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x' -> ['Dm7b5', 'x,5,6,5,6,x', 'x,1,3,2,4,x']

    Input examples:
      'C7    x,3,2,3,1,0    x,3,2,4,1,x'
      'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x'
    """
    cols = split_columns(line)
    if len(cols) < 3:
        raise ValueError(f"Line doesn't contain three columns separated by spaces: {line!r}")

    chord_name = cols[0].strip() # 'Dm7b5'
    frets_str = cols[1].strip() # 'x,5,6,5,6,x'
    fingers_str = cols[2].strip() # 'x,1,3,2,4,x'

    # frets: 'x,5,6,5,6,x' -> [None, 5, 6, 5, 6, None]
    frets_int_lst = global_utilities.crd_slst2ilst(frets_str.split(','))

    # fingers: keep as strings list
    # 'x,1,3,2,4,x' -> ['x', '1', '3', '2', '4', 'x']
    fingers_str_lst = global_utilities.crd_str2slst(fingers_str)

    return chord_name, frets_int_lst, fingers_str_lst


# ------------- VARIABLES -------------------

# copy paste from ods file
trasp_chords_str_lst = (
      'D    x,5,4,2,3,2    x,4,3,1,2,1' 
    , 'F/C    x,3,3,2,1,1    x,3,4,2,1,1'
    ,
    )


# ----------------- MAIN --------------------

if __name__ == "__main__":
    
    trasp_chords_lst = []
    tmp_string = ''
    
    total_out_lines = []
    total_out_lines.append('\n' + DIVIDER_STR)
    total_out_lines.append("")
    total_out_lines.append("Input Chords:")
    total_out_lines.append("-------------")
    
    
    tmp_string = '\n' + DIVIDER_STR + '\n\n' + 'Input Chords:\n-------------'
    print(tmp_string)
    tmp_string = ''
    
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
        chord_name, frets_int_lst, fingers_str_lst = parse_input_line(trasp_chords_str)
        # find root string and maj/min (transportables.find_rootstring_majmin returns (root_note, root_string, majmin))
        # ('D', 5, 'minor') = transportables.find_rootstring_majmin('Dm7b5', [None, 5, 6, 5, 6, None])
        root_note, root_string, majmin = transportables.find_rootstring_majmin(chord_name, frets_int_lst)
        '''
        trasp_chords_lst = [
              ['C7',    [None, 3, 2, 3, 1, 0],    ['x', '3', '2', '4', '1', 'x'], 5, 'major']
            , ['Dm7b5', [None, 5, 6, 5, 6, None], ['x', '1', '3', '2', '4', 'x'], 5, 'minor']
            ]
        '''
        trasp_chords_lst.append([chord_name, frets_int_lst, fingers_str_lst, root_string, majmin])
        tmp_string = ' '.join(
                (
                  '> '
                , '{:<11}'.format(chord_name)
                , '{:<35}'.format(str(frets_int_lst))
                , '{:<35}'.format(str(fingers_str_lst))
                , '{:<7}'.format(str(root_string))
                , majmin
                )
            )
        print(tmp_string)
        total_out_lines.append(tmp_string)
    
    print('\n' + DIVIDER_STR + '\n')
    total_out_lines.append('\n' + DIVIDER_STR + '\n')
    
    
    """
    For each chord in trasp_chords_lst, call transportables.transport and produce output text
    Returns the full accumulated output string.
    """
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
        is_first_print = True
        for chord in chord_list:
            
            if not is_first_print:
                print('\n' + SEP + '\n')
                total_out_lines.append('\n' + SEP + '\n')
                
            is_first_print = False              
            chord_name = chord[0]
            frets_int_lst = chord[1]
            fingers_str_lst = chord[2]
            chord_name_enharm = chord[4]
            
            # chord_parser.parse_chord_name('C7') -> ('C', '7', '', '')
            root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord_name)
            # global_constants.quality_family['7'] > 'Dominant'
            family = global_constants.quality_family[quality]
            latin_root_note = music_utilities.conv_note_en2latin(root_note)
            latin_chord_name = music_utilities.conv_chordname_en2latin(chord_name)
            # [None, 3, 2, 3, 1, None] -> ['x','3','2','3','1','x']
            frets_str = ','.join(global_utilities.crd_ilst2slst(frets_int_lst))
            # ['x', '3', '2', '4', '1', 'x'] -> 'x,3,2,4,1,x'
            fingers_str = ','.join(global_utilities.crd_ilst2slst(fingers_str_lst))
            
            temp_str = '* Txt Latin Output'
            print(temp_str)
            total_out_lines.append(temp_str)
            temp_str = latin_chord_name + '\t' + frets_str + '\t' + fingers_str + '\t%\t%\t%\t' + \
                       latin_root_note + '/' + family
            print(temp_str)
            total_out_lines.append(temp_str)    
            temp_str = '\n* Ods Output'
            print(temp_str)            
            total_out_lines.append(temp_str)    
            temp_str = root_note + '\t' + family + '\t' + quality + '\t' + detail + \
                 '\t' + global_utilities.chain(slash_note, '/', '\t') + \
                 '\t' + global_utilities.lst2str(frets_int_lst, '\t', 'x') + \
                 '\t' + global_utilities.lst2str(fingers_str_lst, '\t', 'x')
            print(temp_str)
            total_out_lines.append(temp_str)    
            if chord_name_enharm:
                root_note_enharm, quality_enharm, detail_enharm, slash_note_enharm = chord_parser.parse_chord_name(chord_name_enharm)
                latin_root_note_enharm = music_utilities.conv_note_en2latin(root_note_enharm)
                latin_chord_name_enharm = music_utilities.conv_chordname_en2latin(chord_name_enharm)
                temp_str = '\n* Txt Latin Enharm Output'
                print(temp_str)
                total_out_lines.append(temp_str)
                temp_str = latin_chord_name_enharm + '\t' + frets_str + '\t' + fingers_str + '\t%\t%\t%\t' + \
                    latin_root_note_enharm + '/' + family
                print(temp_str)
                total_out_lines.append(temp_str)
                temp_str = '\n* Ods Enharm Output'
                print(temp_str)
                total_out_lines.append(temp_str)    
                temp_str = root_note_enharm + '\t' + family + '\t' + quality_enharm + '\t' + detail_enharm + \
                    '\t' + global_utilities.chain(slash_note_enharm, '/', '\t') + \
                    '\t' + global_utilities.lst2str(frets_int_lst, '\t', 'x') + \
                    '\t' + global_utilities.lst2str(fingers_str_lst, '\t', 'x')
                print(temp_str)
                total_out_lines.append(temp_str)    
            
        print('\n' + DIVIDER_STR + '\n')
        total_out_lines.append('\n' + DIVIDER_STR + '\n')
        

fout = open('transp.txt', mode = 'w')
fout.write("\n".join(total_out_lines))
fout.close()

