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
import os

# local application imports
from libs import global_utilities
from libs import scale_parser
from libs import helper_functions
from libs import global_constants



# --- generate scale and scale image (no check scale verbose) ---

# Here we use helper_functions.process_scales_by_config_json() which uses 
# directly scales2files.scale_list_to_files() which draw straight {using
# draw_scales.scale_to_file()} and do not perform any check


# -- input variables --
root_note = 'A'
scale_formula = 'minor_melodic'
json_file_path = './cfg_files/config_scales_7th.json'  # json config file path
scale_upper_fret = 16
dirout = './dirout/'
thumb_width_px = '1100.0px'
display_notes = False
# ---------------------

# generate_scale -> [
#      'A'
#    , 'Minor Melodic Scale'
#    , [[0,   None,  2,   None,  4,    5,  ...], [...], ...]
#    , [['5', None, '6',  None, '7',  'R', ...], [...], ...]
#    , [['E', None, 'Gb', None, 'Ab', 'A', ...], [...], ...]
# ]
(
      root_note
    , scale_name
    , frets
    , intervls
    , notes
) = helper_functions.generate_scale(root_note, scale_formula, scale_upper_fret)

# my_scale_name = 'A Minor Melodic Scale'
my_scale_name = root_note + ' ' + scale_name

# change None to 'x' and number to strings
# ie: [[None,  1,   None,  3,  None ...], ...] -> [['x',  '1',   'x',  '3',  'x' ...], ...]
#     [[None, 'b7', None, 'R', None ...], ...] -> [['x',  'b7',  'x',  'R',  'x' ...], ...]
frets_str =    [[str(elem) if elem is not None else 'x' for elem in strng] for strng in frets]
intervls_str = [[str(elem) if elem is not None else 'x' for elem in strng] for strng in intervls]
notes_str =    [[str(elem) if elem is not None else 'x' for elem in strng] for strng in notes] 

#   my_scale: list of list, each list is a scale:
#   [
#       [
#          error_in_scale
#        , error_message
#        , scale_name
#        , scale_filename
#        , subfolder
#        , strgs_frets_list
#        , strgs_intervals_list
#        , strgs_dlabels_list
#        , footer
#        , arrows
#       ], ..
#   ]
my_scale = [
        [
              False
            , ''
            , my_scale_name
            , my_scale_name
            , ''
            , frets_str
            , intervls_str
            , notes_str if display_notes else intervls_str
            , []
            , []
        ]
    ]

helper_functions.process_scales_by_config_json(
    json_file_path
    , my_scale
    , dir_output = dirout
    , thumb_width = thumb_width_px
    , ncols = 1
    )


# --- generate scale, scale file and scale image (check scale verbose) ---
# Here we use helper_functions.process_scalesfile_by_config_json() which uses 
# scales2files.process_scales_file() which check input file with 
# scale_parser.get_scales_list_from_file() and then
# invoke scale_list_to_files() to draw

# -- input variables --
root_note = 'G'
scale_formula = 'min7_arpeggios'
json_file_path = './cfg_files/config_scales_7th.json'  # json config file path
scale_upper_fret = 16
dirout = './dirout/'
thumb_width_px = '1100.0px'
display_notes = False
# ---------------------

# my_scale = [root_note, scale_name, frets, intervls, notes]
# my_scale = ['G', 'Major Scale', [[0, .....
my_scale = helper_functions.generate_scale(root_note, scale_formula, scale_upper_fret)
# scale_type = 'Major Scale'
scale_type = my_scale[1]
# scale_full_name = 'G Major Scale'
scale_full_name = root_note + ' ' + scale_type
# scale_filename = 'g_major_scale'
scale_filename = global_utilities.lower_and_underscore(scale_full_name)
# scale_filename = './dirout/g_major_scale.txt'
scale_file = dirout + scale_filename + '.txt'


dir_out = os.path.dirname(scale_file)
helper_functions.generate_scale_file(my_scale, scale_file, display_notes)

helper_functions.process_scalesfile_by_config_json(
      json_file_path, scale_file
    , dir_output = os.path.dirname(scale_file)
    , thumb_width = thumb_width_px
    , ncols = 1
    )


# --- generate caged scales, caged scale files and caged scales image (check scale verbose) ---

# caged_params = (
#       ('E Form', 2,  5)
#     , ('D Form', 4,  8)
#     , ('C Form', 7,  10)
#     , ('A Form', 9,  13)
#     , ('G Form', 11, 15)
#     )
caged_params = global_constants.caged_dict[root_note][scale_formula]

# cagedp = ('E Form', 2,  5)
for cagedp in caged_params:
    
    # caged_scale_type = 'Major Scale, E Form'
    caged_scale_type = scale_type  + ', ' +  cagedp[0]
    # caged_scale_full_name = 'G Major Scale, E Form'
    caged_scale_full_name = root_note + ' ' + caged_scale_type
    # caged_scale_filename = 'g_major_scale_e_form'
    caged_scale_filename = global_utilities.sanitize_str(caged_scale_full_name)
    caged_scale_filename = global_utilities.lower_and_underscore(caged_scale_filename)
    # caged_scale_file = './dirout/g_major_scale_e_form.txt'
    caged_scale_file = dirout + caged_scale_filename + '.txt'    

    # scl_list = [
    #        [
    #          error_in_scale
    #        , error_message
    #        , scale_name
    #        , scale_filename
    #        , subfolder
    #        , strgs_frets_list
    #        , strgs_intervals_list
    #        , strgs_dlabels_list
    #        , footer
    #        , arrows
    #       ], 
    #   ]
    scl_list, msg_str = scale_parser.get_scales_list_from_file(scale_file, print_output=True)
    
    myscale = scl_list[0]
    
    strgs_frets_list, strgs_intervals_list, strgs_dlabels_list = myscale[5], myscale[6], myscale[7] 
    lower_slice, upper_slice = cagedp[1], cagedp[2]
    
    caged_t_scale = helper_functions.trunk_scales(
          strgs_frets_list
        , strgs_intervals_list
        , strgs_dlabels_list
        , lower_slice
        , upper_slice
        )
    
    caged_pad_scale = helper_functions.pad_scales(
          caged_t_scale[0] # trunk strgs_frets_list
        , caged_t_scale[1] # trunk strgs_intervals_list
        , caged_t_scale[2] # trunk strgs_dlabels_list
        , 0, scale_upper_fret
        )
    
    helper_functions.generate_scale_file(
          [
                root_note           # 'G'
              , caged_scale_type    # 'Major Scale'
              , caged_pad_scale[0]  # pad strgs_frets_list
              , caged_pad_scale[1]  # pad strgs_intervals_list
              , caged_pad_scale[2]  # pad strgs_dlabels_list
            ]
        , caged_scale_file          # './dirout/g_major_scale_e_form.txt'
        , display_notes
        )
    
    helper_functions.process_scalesfile_by_config_json(
          json_file_path, caged_scale_file
        , dir_output = os.path.dirname(caged_scale_file)
        , thumb_width = thumb_width_px
        , ncols = 1
        , scale_label_isleft = True
        )
