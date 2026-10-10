#!/bin/bash
source /home/simone/MyApps/Dev/myvenv/bin/activate

python3 ../../fancyscales.py '../scls_tests_files/caged_scales.txt' -r='enable' -cf='../json_cfg_tests_files/config_scales.json' -o='./dirout/scales'

python3 ../../fancyscales.py '../scls_tests_files/scales-all-neck.txt' -r='enable' -cf='../json_cfg_tests_files/config_scales_all_neck.json' -o='./dirout/scales_all_neck'

python3 ../../fancyscales.py '../scls_tests_files/caged_scales.txt' -r='enable' -cf='../json_cfg_tests_files/config_scales_all_neck_padded.json' -o='./dirout/scales_all_neck'

deactivate
echo 'Job Done!'