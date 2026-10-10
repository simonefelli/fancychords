#!/bin/bash
source /home/simone/MyApps/Dev/myvenv/bin/activate

python3 ../../fancyscales.py ../scls_tests_files/scale-list.txt -c -rd -r='enable' -o='./output'

python3 ../../fancyscales.py ../scls_tests_files/arpeggios-list.txt -c -rd -r='enable' -o='/home/simone/Documents/dev/python/py3/pychords/app/tests/test_fancyscales/output' -cf='/home/simone/Documents/dev/python/py3/pychords/app/tests/json_cfg_tests_files/config_scales.json'

deactivate
echo 'Job Done!'