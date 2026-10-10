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


# local application imports
from libs import helper_functions


if __name__ == "__main__":
    
    # input variables    
    json_file_path = '../json_cfg_tests_files/config_fancycrds1.json'   # json config file path
    input_crdf = '../crds_test_files/chord-list_fancycrds2.txt'   # path for chord list txt    

    helper_functions.process_chordsfile_by_config_json(
          json_file_path , input_crdf
        , dir_output = './dirout/chords'
        )
    
    # --------------
    
    # input variables    
    json_file_path = '../json_cfg_tests_files/config_caged_chords.json'   # json config file path
    input_crdf = '../crds_test_files/caged_chords.txt'   # path for chord list txt    

    helper_functions.process_chordsfile_by_config_json(
          json_file_path , input_crdf
        , dir_output = './dirout/chords'
        , report = 'enable'
        )
    