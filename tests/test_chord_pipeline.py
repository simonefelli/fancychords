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
Automatic tests for the fancychords and fancyscales pipelines.

Run them from the repository root with:

    python3 -m unittest tests.test_chord_pipeline -v

Unlike the shell scripts in tests/test_fancychords, these tests need no
fixed paths: every file is written in a temporary dir that is deleted at
the end. The end to end tests need svgwrite installed (as fancychords does).
"""

# standard library imports
import json
import os
import subprocess
import sys
import tempfile
import unittest

# local application imports
from libs import autofingers
from libs import chord_parser
from libs import draw_scales
from libs import global_utilities
from libs import intervals
from libs import music_utilities
from libs import scale_parser
from libs import transportables


# repository root dir and fancychords.py path, to run the program as a user would
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FANCYCHORDS = os.path.join(REPO_DIR, 'fancychords.py')
FANCYSCALES = os.path.join(REPO_DIR, 'fancyscales.py')


def run_program(program, *args):
    '''
    run a program (fancychords.py or fancyscales.py) with the given command
    line args and return the CompletedProcess (returncode, stdout, stderr)
    '''
    return subprocess.run(
        [sys.executable, program, *args],
        cwd=REPO_DIR, capture_output=True, text=True
        )


def run_fancychords(*args):
    return run_program(FANCYCHORDS, *args)


def run_fancyscales(*args):
    return run_program(FANCYSCALES, *args)


def scale_block(name, frets, filename='%', intervals=None, dlabels=None):
    '''
    return the text of one scale block for a scale file, with the same
    frets (and optional intervals/dlabels) on all 6 strings
    '''
    string_line = frets
    if intervals: string_line += '\t' + intervals
    if dlabels: string_line += '\t' + (dlabels if intervals else '%\t' + dlabels)
    lines = ['NAME\t' + name, 'FOLDER\t%', 'FILENAME\t' + filename]
    lines += ['STRING0' + str(n) + '\t' + string_line for n in range(1, 7)]
    lines += ['FOOTER\t%', 'ARROWS\t%']
    return '\n'.join(lines) + '\n'


class TestParseChordName(unittest.TestCase):
    '''chord name split in root note, quality, detail and slash note'''

    def test_english_notation(self):
        self.assertEqual(chord_parser.parse_chord_name('Gbmaj9/D#'), ('Gb', 'maj9', '', 'D#'))

    def test_latin_notation(self):
        self.assertEqual(chord_parser.parse_chord_name('FA#m(no5)/SOLb'), ('FA#', 'm', '(no5)', 'SOLb'))

    def test_latin_sol_has_three_letters(self):
        self.assertEqual(chord_parser.parse_chord_name('SOLm7'), ('SOL', 'm7', '', ''))


class TestCheckCrdParams(unittest.TestCase):
    '''validation of a single chord'''

    def test_blank_chord_name_is_an_error_not_a_crash(self):
        # before the fix this raised UnboundLocalError and stopped the whole run
        result = chord_parser.check_crd_params('', 'x,3,2,0,1,0', '', '', '', '', '')
        self.assertTrue(result[0])

    def test_wrong_frets_are_rejected(self):
        result = chord_parser.check_crd_params('C', 'x,3,2,0,1', '', '', '', '', '')
        self.assertTrue(result[0])

    def test_plus_is_kept_in_filename(self):
        # chord_filename is element 4 of the returned tuple
        result = chord_parser.check_crd_params('LA7+sus2', 'x,0,2,1,0,0', '', '', '', '', '')
        self.assertEqual(result[4], 'LA7+sus2')

    def test_slash_becomes_underscore_in_filename(self):
        result = chord_parser.check_crd_params('G#dim7(no5)/F#', '2,2,0,1,0,1', '', '', '', '', '')
        self.assertEqual(result[4], 'G#dim7no5_F#')


class TestFixDuplicateChordnames(unittest.TestCase):
    '''every chord must get its own output file name'''

    @staticmethod
    def names(filenames):
        # build a minimal crd_list: only index 2 (chord_filename) is used
        crd_list = [[name, '', name] for name in filenames]
        return [crd[2] for crd in chord_parser.fix_duplicate_chordnames(crd_list)]

    def test_duplicates_get_version_postfix(self):
        self.assertEqual(self.names(['Cm', 'Cm', 'Cm']), ['Cm', 'Cm.v02', 'Cm.v03'])

    def test_names_differing_only_by_case_are_duplicates(self):
        # on Windows/macOS Cm7.svg and CM7.svg are the same file
        self.assertEqual(self.names(['Cm7', 'CM7']), ['Cm7', 'CM7.v02'])

    def test_generated_name_never_clashes_with_given_name(self):
        self.assertEqual(self.names(['Cm', 'Cm.v02', 'Cm']), ['Cm', 'Cm.v02', 'Cm.v03'])


class TestParamCheck(unittest.TestCase):
    '''cli > json config file > default precedence'''

    defaults = {'horiz': False}

    def test_default(self):
        self.assertEqual(global_utilities.param_check({}, None, 'horiz', 'flags', self.defaults), (False, True))

    def test_json_wins_over_default(self):
        jdump = {'flags': {'horiz': True}}
        self.assertEqual(global_utilities.param_check(jdump, None, 'horiz', 'flags', self.defaults), (True, False))

    def test_cli_wins_over_json(self):
        jdump = {'flags': {'horiz': True}}
        self.assertEqual(global_utilities.param_check(jdump, False, 'horiz', 'flags', self.defaults), (False, True))

    def test_empty_json_section(self):
        # before the fix '"flags": {}' raised UnboundLocalError
        jdump = {'flags': {}}
        self.assertEqual(global_utilities.param_check(jdump, None, 'horiz', 'flags', self.defaults), (False, True))


class TestFancychordsEndToEnd(unittest.TestCase):
    '''run the real program and check the files it writes'''

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def svg_files(self, subdir=''):
        return sorted(f for f in os.listdir(os.path.join(self.out, subdir)) if f.endswith('.svg'))

    def test_chords_differing_by_plus_both_written(self):
        result = run_fancychords('--cli_in=LA7sus2|x,0,2,0,0,0;LA7+sus2|x,0,2,1,0,0', '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(), ['LA7+sus2.svg', 'LA7sus2.svg'])

    def test_trailing_semicolon_is_ignored(self):
        result = run_fancychords('--cli_in=C|x,3,2,0,1,0; ', '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(), ['C.svg'])

    def test_empty_cli_field_works_like_percent(self):
        # 'C|frets||intervals': the empty field is fingers, intervals stay intervals
        result = run_fancychords('--cli_in=C|x,3,2,0,1,0||x,R,3,5,R,3', '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Loaded', result.stdout)
        self.assertEqual(self.svg_files(), ['C.svg'])

    def test_subfolder(self):
        result = run_fancychords('--cli_in=C|x,3,2,0,1,0|%|%|%|%|C/Major', '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(os.path.join('C', 'Major')), ['C.svg'])

    def test_file_input(self):
        chords_file = os.path.join(self.out, 'chords.txt')
        with open(chords_file, 'w', encoding='utf-8') as f:
            f.write('// comment line\n')
            f.write('NAME\t\tFRETS\t\tFINGERS\n')
            f.write('C\t\tx,3,2,0,1,0\t\tx,3,2,x,1,x\n')
            f.write('G\t\t3,2,0,0,0,3\t\t2,1,x,x,x,3\n')
        result = run_fancychords('--file_in=' + chords_file, '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(), ['C.svg', 'G.svg'])

    def test_missing_input_file_fails_with_exit_status_1(self):
        result = run_fancychords('--file_in=' + os.path.join(self.out, 'nope.txt'), '-o', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn('fancychords error', result.stderr)

    def test_json_config_with_partial_formats(self):
        # a fretb_format with only '*' (no 'r') used to raise KeyError
        config = {'generic_formats': {'fretb_format': {
            '*': [1.0, 'black', '1.0', 'black', '1.0', 'none', '3.0', 'white', '1.0', '', '', False, False]
            }}}
        config_file = os.path.join(self.out, 'config.json')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f)
        result = run_fancychords('--cli_in=C|x,3,2,0,1,0', '-cf', config_file, '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(), ['C.svg'])


class TestScalesSideLabels(unittest.TestCase):
    '''fret numbers on the side of scale diagrams'''

    def test_open_position(self):
        self.assertEqual(draw_scales.scales_side_labels(0, 5), [None, None, '3', None, '5'])

    def test_scale_on_a_single_fret(self):
        # first_fret == max_fret used to raise IndexError
        self.assertEqual(draw_scales.scales_side_labels(5, 5), ['5'])

    def test_frets_above_21(self):
        # the label table stopped at fret 21, frets 22..24 raised IndexError
        self.assertEqual(draw_scales.scales_side_labels(22, 24), ['22', None, '24'])


class TestCheckScaleParams(unittest.TestCase):
    '''validation of a single scale'''

    @staticmethod
    def check(frets, intervals='', dlabels='', filename='', name='Test'):
        strings = [[frets, intervals, dlabels]] * 6
        return scale_parser.check_scl_params(name, '', filename, *strings, '', '')

    def test_good_scale(self):
        self.assertFalse(self.check('5,x,7', 'R,x,2', '1,x,3')[0])

    def test_dlabels_length_checked_without_intervals(self):
        # dlabels with a different number of columns than frets must be an
        # error even when intervals are not given
        result = self.check('5,x,7', '', '1,x')
        self.assertTrue(result[0])
        self.assertIn('dlabels', result[1])

    def test_percent_filename_means_use_scale_name(self):
        # element 3 is scale_filename, it used to be '' (saved as '.svg')
        self.assertEqual(self.check('5,x,7', filename='%', name='Am Blues')[3], 'Am Blues')


class TestFancyscalesEndToEnd(unittest.TestCase):
    '''run the real fancyscales program'''

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def write_scales(self, *blocks):
        scales_file = os.path.join(self.out, 'scales.txt')
        with open(scales_file, 'w', encoding='utf-8') as f:
            f.write(''.join(blocks))
        return scales_file

    def svg_files(self):
        return sorted(f for f in os.listdir(self.out) if f.endswith('.svg'))

    def test_duplicate_scale_names_get_version_postfix(self):
        scales_file = self.write_scales(scale_block('Am', '5,x,7'), scale_block('Am', '7,x,9'))
        result = run_fancyscales(scales_file, '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(), ['Am.svg', 'Am.v02.svg'])

    def test_dots_above_nut(self):
        # -n (dots above the nut) used to fail: fret0 dots got '' as font weight
        scales_file = self.write_scales(scale_block('Open', '0,2,3', intervals='R,2,b3'))
        result = run_fancyscales(scales_file, '-n', '-o', self.out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.svg_files(), ['Open.svg'])

    def test_missing_input_file_fails_with_exit_status_1(self):
        result = run_fancyscales(os.path.join(self.out, 'nope.txt'), '-o', self.out)
        self.assertEqual(result.returncode, 1)
        self.assertIn('fancyscales error', result.stderr)


class TestMusicTheory(unittest.TestCase):
    '''music_utilities, intervals, autofingers, transportables'''

    def test_latin_chord_without_slash(self):
        # 'LAm7' used to become 'Am7/' (with a stray slash)
        self.assertEqual(music_utilities.is_latin_chord('LAm7'), (True, 'Am7'))
        self.assertEqual(music_utilities.is_latin_chord('SOLb/REb'), (True, 'Gb/Db'))

    def test_note_on_24th_fret(self):
        # low E string, 24th fret is E again (two octaves up); it raised IndexError
        self.assertEqual(music_utilities.singl_fret_to_note(6, 24, 'sharp'), 'E')

    def test_lowest_root_with_unknown_quality(self):
        # a quality not in formulas_list used to raise KeyError
        self.assertEqual(music_utilities.lowest_root_in_chord('Cxyz', [None, 3, 2, 0, 1, 0]), 5)

    def test_chord_finder_no_match_keeps_bass_note(self):
        # no formula matches this chord: bass note is still C, the root
        result = intervals.chord_finder('C', [None, 3, 2, 3, 0, 7])[0]
        self.assertIsNone(result[0])
        self.assertEqual((result[9], result[10]), (True, 'C'))
        self.assertEqual(result[4][1], 'C')

    def test_autofingers_common_chords(self):
        self.assertEqual(autofingers.chord_autofingers(['x', '2', '4', '4', '3', '2']), ['x', '1', '3', '4', '2', '1'])

    def test_autofingers_shadowed_two_strings_barre(self):
        # raised TypeError (expand_fr_clst returned a tuple instead of a list)
        self.assertEqual(autofingers.chord_autofingers(['3', '2', 'x', '3', '4', '5']), ['2', '1', 'x', '3', '4', 'x'])

    def test_autofingers_more_than_4_fingers(self):
        # raised IndexError: strings that cannot be fingered stay 'x'
        self.assertEqual(autofingers.chord_autofingers(['1', '2', '3', '4', '5', '6']), ['1', '2', '3', '4', 'x', 'x'])

    def test_transport_keeps_open_strings_of_original_chord(self):
        chords = transportables.transport(('C7', [None, 3, 2, 3, 1, 0], ['x', '3', '2', '4', '1', 'x'], 5, 'major'))
        # the chord itself keeps its open high e
        self.assertEqual(chords[0][:2], ('C7', [None, 3, 2, 3, 1, 0]))
        # shifted chords drop open strings (they cannot move with the shape)
        self.assertEqual(chords[1][:2], ('C#7', [None, 4, 3, 4, 2, None]))


if __name__ == '__main__':
    unittest.main()
