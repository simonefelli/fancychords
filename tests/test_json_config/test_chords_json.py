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


# standard library imports
import json


json_file_path = '../json_cfg_tests_files/config.json'
# json_file_path = 'C:\\Users\\sfelli\\simo\\dev\\python\\py3\\pychords\\app\\tests\\json_cfg_tests_files\\config.json'


with open(json_file_path, 'r') as jsonfile:
    db_dict_jdump = json.load(jsonfile)

io_dict = db_dict_jdump['i/o']
flags_dict = db_dict_jdump['flags']
format_dict = db_dict_jdump['generic_formats']
parameters_dict = db_dict_jdump['parameters']


len_io_dict = len(io_dict)
len_flags_dict = len(flags_dict)
len_format_dict = len(format_dict)
len_parameters_dict = len(parameters_dict)

print('config file:\n------------')
print('file path:', json_file_path)
print('num total variables:', len_io_dict + len_flags_dict + len_format_dict + len_parameters_dict)
print('num sections:', len(db_dict_jdump.keys()))

print('\n\nparameters_dict (' + str(len_parameters_dict) + ' elements):\n------------------------------')
for key, val in parameters_dict.items(): print(key, ' -> ', val)

print('\n\nio_dict (' + str(len_io_dict) + ' elements):\n---------------------')
for key, val in io_dict.items(): print(key, ' -> ', val)

print('\n\nflags_dict (' + str(len_flags_dict) + ' elements):\n-------------------------')
for key, val in flags_dict.items(): print(key, ' -> ', val)

print('\n\nformat_dict (' + str(len_flags_dict) + ' elements):\n--------------------------')
for key, val in format_dict.items(): print(key, ' -> ', str(val)[:80])


# -- parameters --
barre_strk_wdth = parameters_dict.get('barre_strk_wdth')
lntk = parameters_dict['lntk']
x_or = parameters_dict['x_or']
y_or = parameters_dict['y_or']
ns = parameters_dict['ns']
nf = parameters_dict['nf']
fd = parameters_dict.get('fd')
sd = parameters_dict['sd']
radius_factor = parameters_dict.get('radius_factor')
ncols = parameters_dict['ncols']
thumb_width = parameters_dict['thumb_width']
# -- directory out --
dir_output = io_dict['dir_output']
# -- flags --
horiz = flags_dict['horiz']
chord_label_isbottom = flags_dict['chord_label_isbottom']
chord_label_isleft = flags_dict['chord_label_isleft']
enable_header = flags_dict['enable_header']
enable_dotlabels = flags_dict['enable_dotlabels']
enable_footer = flags_dict['enable_footer']
enable_barre = flags_dict['enable_barre']
enable_fretnum = flags_dict['enable_fretnum']
nutline = flags_dict['nutline']
fret0 = flags_dict['fret0']
convert_flag = flags_dict['convert_flag']
report = flags_dict['report']
debug = flags_dict['debug']
root_is_different = flags_dict['root_is_different']
# -- generic_formats --
font_weight = format_dict['font_weight']
font_family = format_dict['font_family']
chord_label_font_weight = format_dict['chord_label_font_weight']
chord_label_font_family = format_dict['chord_label_font_family']
chord_label_font_factor = format_dict['chord_label_font_factor']
upper_labels_font_weight = format_dict['upper_labels_font_weight']
upper_labels_font_family = format_dict['upper_labels_font_family']
upper_labels_font_factor = format_dict['upper_labels_font_factor']
bottom_labels_font_weight = format_dict['bottom_labels_font_weight']
bottom_labels_font_family = format_dict['bottom_labels_font_family']
bottom_labels_font_factor = format_dict['bottom_labels_font_factor']
side_labels_font_weight = format_dict['side_labels_font_weight']
side_labels_font_family = format_dict['side_labels_font_family']
side_labels_font_factor = format_dict['side_labels_font_factor']
fretb_format = format_dict['fretb_format']
fret0_format = format_dict['fret0_format']

'''
params not used in chords2files but present in json config file
- root_is_different

params used inside process_chords() but not present in json config file
- input_way

params used inside process_chords() and inside generate_htmlreport()
- dir_output

params used outside process_chords() to generate htmlreport
- report
- ncols
- thumb_width
'''

args = (
    dir_output, horiz, enable_header, enable_dotlabels, 
    enable_footer, enable_barre, enable_fretnum,
    barre_strk_wdth, nutline, fret0,
    font_weight, font_family,
    chord_label_font_weight, chord_label_font_family, 
    chord_label_font_factor, chord_label_isbottom, chord_label_isleft,
    fretb_format, fret0_format,
    upper_labels_font_weight, upper_labels_font_family, upper_labels_font_factor, 
    bottom_labels_font_weight, bottom_labels_font_family, bottom_labels_font_factor, 
    side_labels_font_weight, side_labels_font_family, side_labels_font_factor,
    lntk, x_or, y_or, ns, nf, fd, sd, radius_factor, 
    convert_flag, debug
    )

print('\ntotal args:\n', args)

# -- derived variables tests ---

print('\n\nderived variables:\n------------------')

if not fd:
    db_dict_jdump['parameters']['fd'] = sd * 1.30
    print('* fd:', db_dict_jdump['parameters']['fd'])

if not radius_factor:
    db_dict_jdump['parameters']['radius_factor'] = 20.00 / sd
    print('* radius_factor:', db_dict_jdump['parameters']['radius_factor'])

if not barre_strk_wdth:
    db_dict_jdump['parameters']['barre_strk_wdth'] = 1.10 * lntk
    print('* barre_strk_wdth:', db_dict_jdump['parameters']['barre_strk_wdth'])

