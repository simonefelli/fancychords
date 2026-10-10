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
Improved transport_chords.py

Highlights:
- More modular: functions with clear responsibilities and type hints.
- Robust parsing: tolerates variable whitespace between columns (uses regex).
- CLI: small argparse interface (use default sample data if no file provided).
- Safer file handling (with open(...)).
- Fixed bug: proper file close and more readable output assembly.
- Better logging of errors while keeping similar printed output.
"""

from typing import List, Optional, Tuple
import re
import argparse
from pathlib import Path
import sys

from libs import global_constants
from libs import global_utilities
from libs import music_utilities
from libs import chord_parser
from libs import transportables


DIVIDER_STR = '##########################################################################\n'


def split_columns(line: str) -> List[str]:
    """
    Split a line into columns using at least 4 spaces as separator (like original script).
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
    frets_list = global_utilities.crd_slst2ilst(frets_str.split(','))

    # fingers: keep as strings list
    fingers_list = global_utilities.crd_str2slst(fingers_str)

    return chord_name, frets_list, fingers_list


def build_initial_list(lines: List[str]) -> List[List]:
    """
    Convert input lines into the initial trasp_chords_lst structure used later.
    Each entry: [chord_name, frets_int_lst, fingers_str_lst, root_string, majmin]
    """
    trasp_chords_lst = []
    for line in lines:
        if not line or not line.strip():
            continue
        try:
            chord_name, frets_int_lst, fingers_str_lst = parse_input_line(line)
            # find root string and maj/min (transportables.find_rootstring_majmin returns (root_note, root_string, majmin))
            root_note, root_string, majmin = transportables.find_rootstring_majmin(chord_name, frets_int_lst)
            trasp_chords_lst.append([chord_name, frets_int_lst, fingers_str_lst, root_string, majmin])
        except Exception as exc:
            # keep processing other lines but inform the user
            print(f"Warning: failed to parse line: {line!r}\n  {exc}", file=sys.stderr)
    return trasp_chords_lst


def process_transpositions(trasp_chords_lst: List[List]) -> str:
    """
    For each chord in trasp_chords_lst, call transportables.transport and produce output text
    comparable to the original script. Returns the full accumulated output string.
    """
    total_out_lines: List[str] = []
    total_out_lines.append(DIVIDER_STR)
    total_out_lines.append("")
    total_out_lines.append("Input Chords:")
    total_out_lines.append("-------------")

    # Print initial summary for each input chord
    for chord_entry in trasp_chords_lst:
        chord_name, frets_int_lst, fingers_str_lst, root_string, majmin = chord_entry
        tmp = (
            f"> {chord_name:<11} {str(frets_int_lst):<35} {str(fingers_str_lst):<35} "
            f"{str(root_string):<7} {majmin}"
        )
        print(tmp)
        total_out_lines.append(tmp)

    total_out_lines.append("")
    total_out_lines.append(DIVIDER_STR)

    is_first_print = True

    for trasp_chord in trasp_chords_lst:
        chord_list = transportables.transport(trasp_chord)
        for chord in chord_list:
            if not is_first_print:
                sep = '\n===================================\n'
                print(sep)
                total_out_lines.append(sep)
            is_first_print = False

            chord_name = chord[0]
            chord_name_enharm = chord[4]

            root_note, quality, detail, slash_note = chord_parser.parse_chord_name(chord_name)
            family = global_constants.quality_family.get(quality, '')
            latin_root_note = music_utilities.conv_note_en2latin(root_note)
            latin_chord_name = music_utilities.conv_chordname_en2latin(chord_name)

            frets_str = ','.join(global_utilities.crd_ilst2slst(chord[1]))
            fingers_str = ','.join(global_utilities.crd_ilst2slst(chord[2]))

            # Txt Latin Output
            total_out_lines.append('* Txt Latin Output')
            print('* Txt Latin Output')
            line_txt = f"{latin_chord_name}\t{frets_str}\t{fingers_str}\t%\t%\t%\t{latin_root_note}/{family}"
            print(line_txt)
            total_out_lines.append(line_txt)

            # Ods Output
            total_out_lines.append('* Ods Output')
            print('* Ods Output')
            ods_line = (
                f"{root_note}\t{family}\t{quality}\t{detail}\t"
                f"{global_utilities.chain(slash_note, '/', '\t')}\t"
                f"{global_utilities.lst2str(chord[1], '\t', 'x')}\t"
                f"{global_utilities.lst2str(chord[2], '\t', 'x')}"
            )
            print(ods_line)
            total_out_lines.append(ods_line)

            # Enharmonic outputs (if present)
            if chord_name_enharm:
                root_note_enharm, quality_enharm, detail_enharm, slash_note_enharm = chord_parser.parse_chord_name(chord_name_enharm)
                latin_root_note_enharm = music_utilities.conv_note_en2latin(root_note_enharm)
                latin_chord_name_enharm = music_utilities.conv_chordname_en2latin(chord_name_enharm)

                total_out_lines.append('* Txt Latin Enharm Output')
                print('* Txt Latin Enharm Output')
                enh_txt = f"{latin_chord_name_enharm}\t{frets_str}\t{fingers_str}\t%\t%\t%\t{latin_root_note_enharm}/{family}"
                print(enh_txt)
                total_out_lines.append(enh_txt)

                total_out_lines.append('* Ods Enharm Output')
                print('* Ods Enharm Output')
                enh_ods = (
                    f"{root_note_enharm}\t{family}\t{quality_enharm}\t{detail_enharm}\t{slash_note_enharm}\t"
                    f"{global_utilities.lst2str(chord[1], '\t', 'x')}\t"
                    f"{global_utilities.lst2str(chord[2], '\t', 'x')}"
                )
                print(enh_ods)
                total_out_lines.append(enh_ods)

    total_out_lines.append("")
    total_out_lines.append(DIVIDER_STR)
    return "\n".join(total_out_lines)


def read_input_file(path: Path) -> List[str]:
    """
    Read lines from a file and return non-empty lines.
    """
    lines = []
    with path.open(encoding='utf-8') as fh:
        for raw in fh:
            s = raw.strip()
            if s:
                lines.append(s)
    return lines


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Transpose chords and produce output similar to original script.")
    parser.add_argument('-i', '--input', type=Path, help='Input file with chord lines (one per line). If omitted, sample data is used.')
    parser.add_argument('-o', '--output', type=Path, default=Path('transp.txt'), help='Output file (default: transp.txt).')
    args = parser.parse_args(argv)

    sample_lines = [
        'D    x,5,4,2,3,2    x,4,3,1,2,1',
        'F    1,3,3,2,1,1    1,3,4,2,1,1',
    ]

    if args.input:
        try:
            input_lines = read_input_file(args.input)
        except Exception as exc:
            print(f"Error reading input file {args.input}: {exc}", file=sys.stderr)
            return 2
        if not input_lines:
            print(f"Input file {args.input} contains no valid lines, using sample data.", file=sys.stderr)
            input_lines = sample_lines
    else:
        input_lines = sample_lines

    trasp_chords_lst = build_initial_list(input_lines)
    output_text = process_transpositions(trasp_chords_lst)

    try:
        with args.output.open('w', encoding='utf-8') as fout:
            fout.write(output_text)
            fout.write('\n')
            fout.write(DIVIDER_STR)
        print(f"\nWrote output to {args.output}")
    except Exception as exc:
        print(f"Error writing output file {args.output}: {exc}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())