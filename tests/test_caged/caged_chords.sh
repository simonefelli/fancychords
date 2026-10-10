#!/bin/bash
source /home/simone/MyApps/Dev/myvenv/bin/activate
python3 ../../fancychords.py --file_in='../crds_test_files/caged_chords.txt' -r='enable' -cf='../json_cfg_tests_files/config_caged_chords.json' -o='./dirout/chords'
deactivate
echo 'Job Done!'
