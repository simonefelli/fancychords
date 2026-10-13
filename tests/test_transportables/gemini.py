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


# --------------- IMPORTS -------------------

# builtin libs
import re
from typing import List, Tuple, Optional, Any

# --- External Libs ---
# Assuming these libs exist in a 'libs' directory
from libs import global_constants
from libs import global_utilities
from libs import music_utilities
from libs import chord_parser
from libs import transportables


# -------------- CONSTANTS ------------------

DIVIDER_STR = '#' * 74
SEP = '=' * 35


# -------------- FUNCTIONS ------------------

def split_columns(line: str) -> List[str]:
    """
    Split a line into columns using at least 4 spaces as separator.
    Falls back to splitting on any sequence of whitespace if needed.
    """
    cols = re.split(r'\s{4,}', line.strip())
    if len(cols) == 1:
        cols = re.split(r'\s+', line.strip())
    return cols


def parse_input_line(line: str) -> Tuple[str, List[Optional[int]], List[str]]:
    """
    Parse a single input line into (chord_name, frets_int_list, fingers_str_list).
    
    Input examples:
      'C7    x,3,2,3,1,0    x,3,2,4,1,x'
      'Dm7b5    x,5,6,5,6,x    x,1,3,2,4,x'
    """
    cols = split_columns(line)
    if len(cols) < 3:
        raise ValueError(f"Line doesn't contain three columns separated by spaces: {line!r}")

    chord_name = cols[0].strip()
    frets_str = cols[1].strip()
    fingers_str = cols[2].strip()

    # frets: 'x,5,6,5,6,x' -> [None, 5, 6, 5, 6, None]
    frets_int_lst = global_utilities.crd_slst2ilst(frets_str.split(','))

    # fingers: 'x,1,3,2,4,x' -> ['x', '1', '3', '2', '4', 'x']
    fingers_str_lst = global_utilities.crd_str2slst(fingers_str)

    return chord_name, frets_int_lst, fingers_str_lst


def format_chord_output_lines(chord_name: str, frets_list: List[Optional[int]], fingers_list: List[str]) -> List[str]:
    """
    Generates all output lines (Latin, Ods) for a single chord.
    This helper function prevents code duplication for enharmonic chords.
    """
    output_lines = []
    
    # --- Parse Chord ---
    # chord_parser.parse_chord_name('C7') -> ('C', '7', '', '')
    root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord_name)
    
    # global_constants.quality_family['7'] > 'Dominant'
    family = global_constants.quality_family.get(quality, 'Unknown')
    
    # --- Conversions ---
    latin_root_note = music_utilities.conv_note_en2latin(root_note)
    latin_chord_name = music_utilities.conv_chordname_en2latin(chord_name)
    
    # [None, 3, 2, 3, 1, None] -> 'x,3,2,3,1,x'
    frets_str = ','.join(global_utilities.crd_ilst2slst(frets_list))
    # ['x', '3', '2', '4', '1', 'x'] -> 'x,3,2,4,1,x'
    fingers_str = ','.join(global_utilities.crd_ilst2slst(fingers_list))

    # --- Build Output Strings ---
    
    # * Txt Latin Output
    output_lines.append('* Txt Latin Output')
    # Using '\t' separator for Txt output. The '%\t%\t%' is preserved from original.
    output_lines.append(
        f"{latin_chord_name}\t{frets_str}\t{fingers_str}\t%\t%\t%\t{latin_root_note}/{family}"
    )
    
    # * Ods Output
    output_lines.append('\n* Ods Output')
    ods_parts = [
        root_note,
        family,
        quality,
        detail,
        global_utilities.chain(slash_note, '/', ''),
        global_utilities.lst2str(frets_list, '\t', 'x'),
        global_utilities.lst2str(fingers_list, '\t', 'x')
    ]
    # Filter out empty strings from parts like 'detail' or 'slash_note'
    output_lines.append("\t".join(part for part in ods_parts if part))
    
    return output_lines


def main():
    """
    Main script logic:
    1. Parse input chords.
    2. Transport each chord.
    3. Format all outputs.
    4. Print to console and write to file.
    """
    
    # copy paste from ods file
    trasp_chords_str_lst = (
          'D    x,5,4,2,3,2    x,4,3,1,2,1' 
        , 'F    1,3,3,2,1,1    1,3,4,2,1,1'
        ,
    )
    
    trasp_chords_lst = []
    total_out_lines = []
    
    
    # --- 1. Parse Input Chords ---
    
    total_out_lines.append(f'\n{DIVIDER_STR}\n')
    total_out_lines.append("Input Chords:")
    total_out_lines.append("-------------")
    
    for trasp_chords_str in trasp_chords_str_lst:
        if not trasp_chords_str.strip():
            continue  # Skip empty lines

        chord_name, frets_int_lst, fingers_str_lst = parse_input_line(trasp_chords_str)
        
        # find root string and maj/min
        root_note, root_string, majmin = transportables.find_rootstring_majmin(chord_name, frets_int_lst)
        
        trasp_chords_lst.append([chord_name, frets_int_lst, fingers_str_lst, root_string, majmin])
        
        # Format input line for printing
        out_line = (
            f'> {chord_name:<11} {str(frets_int_lst):<35} '
            f'{str(fingers_str_lst):<35} {str(root_string):<7} {majmin}'
        )
        total_out_lines.append(out_line)
    
    total_out_lines.append(f'\n{DIVIDER_STR}\n')
    
    
    # --- 2. Transport & 3. Format Chords ---
    
    for trasp_chord in trasp_chords_lst:
        # transportables.transport returns a list of transported chords
        # e.g., [('C7', ...), ('C#7', ...), ('D7', ...)]
        chord_list: List[Tuple[str, List, List, List, Optional[str]]] = transportables.transport(trasp_chord)
        
        output_blocks = []
        for chord_data in chord_list:
            chord_lines = []
            chord_name = chord_data[0]
            frets_list = chord_data[1]
            fingers_list = chord_data[2]
            chord_name_enharm = chord_data[4] # Enharmonic name, if any

            # Add lines for the main chord name
            chord_lines.extend(
                format_chord_output_lines(chord_name, frets_list, fingers_list)
            )
            
            # Add lines for the enharmonic chord name, if it exists
            if chord_name_enharm:
                chord_lines.append("") # Add a newline
                chord_lines.extend(
                    format_chord_output_lines(chord_name_enharm, frets_list, fingers_list)
                )
            
            output_blocks.append("\n".join(chord_lines))
        
        # Join all transported chords (C7, C#7, etc.) with the separator
        total_out_lines.append(f"\n\n{SEP}\n\n".join(output_blocks))
        total_out_lines.append(f'\n{DIVIDER_STR}\n')
        

    # --- 4. Print to Console and Write to File ---
    
    output_filename = 'transp.txt'
    final_output = "\n".join(total_out_lines)
    
    # Print entire result to console
    print(final_output)
    
    # Safely write to file using 'with'
    try:
        with open(output_filename, mode='w', encoding='utf-8') as fout:
            fout.write(final_output)
        print(f"\nSuccessfully wrote output to {output_filename}")
    except IOError as e:
        print(f"\nError writing to file {output_filename}: {e}")


# ----------------- MAIN --------------------

if __name__ == "__main__":
    main()