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
from libs import helper_functions



if __name__ == "__main__":
    
    # testing this generate_scale function   
    
    # -------------------------
    
    my_scale = helper_functions.generate_scale('G', 'minor_blues_scale', 16)
    (
        root_note, scale_name, neck_frets_fltrd,
        neck_intervls_fltrd, neck_notes_fltrd
    ) = my_scale
    scale_file = './dirout/scales/myscale.txt'  
    helper_functions.generate_scale_file(my_scale, scale_file, False)

    # input variables    
    json_file_path = '../json_cfg_tests_files/config_scales.json'   # json config file path
    helper_functions.process_scalesfile_by_config_json(
          json_file_path , scale_file
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        )

    # -------------------------
    
    my_scale = helper_functions.generate_scale('Ab', 'minor_natural', 16)
    (
        root_note, scale_name, neck_frets_fltrd,
        neck_intervls_fltrd, neck_notes_fltrd
    ) = my_scale
    scale_file = './dirout/scales/myscale.txt'  
    helper_functions.generate_scale_file(my_scale, scale_file, False)

    # input variables    
    json_file_path = '../json_cfg_tests_files/config_scales.json'   # json config file path
    helper_functions.process_scalesfile_by_config_json(
          json_file_path , scale_file
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        )
    
    # -------------------------
    
    my_scale = helper_functions.generate_scale('A', 'min7b5_arpeggios', 16)
    (
        root_note, scale_name, neck_frets_fltrd,
        neck_intervls_fltrd, neck_notes_fltrd
    ) = my_scale
    scale_file = './dirout/scales/myscale.txt'  
    helper_functions.generate_scale_file(my_scale, scale_file, False)

    # input variables    
    json_file_path = '../json_cfg_tests_files/config_scales.json'   # json config file path
    helper_functions.process_scalesfile_by_config_json(
          json_file_path , scale_file
        , dir_output = os.path.dirname(scale_file)
        , thumb_width = '1100.0px'
        , report = 'enable'
        , ncols = 1
        )
    
    # -------------------------