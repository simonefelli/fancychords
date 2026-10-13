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


# local application imports
from libs import helper_functions


if __name__ == "__main__":
    
    # input variables    
    json_file_path = '../json_cfg_tests_files/default_scales_config.json'   # json config file path
    input_sclf = '../scls_tests_files/arpeggios-list.txt'   # path for scale list txt    

    helper_functions.process_scalesfile_by_config_json(
          json_file_path , input_sclf
        , dir_output = './dirout/scales'
        )
    
    # --------------
    
    # input variables    
    json_file_path = '../json_cfg_tests_files/config_scales.json'   # json config file path
    input_sclf = '../scls_tests_files/caged_scales.txt'   # path for scale list txt    

    helper_functions.process_scalesfile_by_config_json(
          json_file_path , input_sclf
        , dir_output = './dirout/scales'
        , report = 'enable'
        )
    