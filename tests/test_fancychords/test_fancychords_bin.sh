#!/bin/bash
source /home/simone/MyApps/Dev/myvenv/bin/activate


# --file_in and check absolute/relative paths

../../fancychords --file_in=../crds_test_files/chord-list_fancycrds1.txt -c -rd -r='enable' -o='/home/simone/Documents/dev/python/py3/pychords/app/tests/test_fancychords/output'

../../fancychords --file_in='/home/simone/Documents/dev/python/py3/pychords/app/tests/crds_test_files/chord-list_fancycrds2.txt' -c -rd -r='enable' -cf='/home/simone/Documents/dev/python/py3/pychords/app/tests/json_cfg_tests_files/config_fancycrds1.json'


# --cli_in & duplicate chord name & -cf=./config.json

../../fancychords --cli_in='Csus1(noconv)|x,0,0,2,1,0|%|%|%|%|C/Sus;Csus1(noconv)|x,1,3,3,2,1|%|%|%|%|C/Sus' -r='enable' -o='./output'

../../fancychords --cli_in='Csus2|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3h,5|%|x,1,3,4,2,1|C/Sus' -ft -cf='../json_cfg_tests_files/config_fancycrds2.json'

../../fancychords --cli_in='Csus3|3,2,0,0,0,1|3,2,x,x,x,1|R,3,5,R,3,7|%|3,2,x,x,x,1|C/Sus' -n -ft -cf='../json_cfg_tests_files/config_fancycrds2.json'

../../fancychords --cli_in='Csus4|0,0,2,2,2,3|x,x,1,2,3,x|5,R,5,R,3,b7h|%|x,x,1,2,3,x|C/Sus' -n -ft -cf='../json_cfg_tests_files/config_fancycrds2.json'

../../fancychords --cli_in='Csus5|0,0,2,2,2,3|x,x,1,2,3,x|5,R,5,R,3,b7h|%|x,x,1,2,3,x|C/Sus' -n -ft -cf='../json_cfg_tests_files/config_fancycrds2.json' -ho

../../fancychords --cli_in='Csus6|0,1,3,3,2,1|x,1,3,4,2,1|5,R,5,Rh,b3,5|%|x,1,3,4,2,1|C/Sus' -n -ft -cf='../json_cfg_tests_files/config_fancycrds2.json'

../../fancychords --cli_in='Csus7|0,1,3,3,2,1|x,1,3,4,2,1|5,R,5,Rh,b3,5|%|x,1,3,4,2,1|C/Sus' -n -ft -cf='../json_cfg_tests_files/config_fancycrds2.json' -ho


# --cli_in & increase stuff

../../fancychords --cli_in='Dsus1(noconv)|x,1,3,3,2,1|x,1,3,4,2,1|%|%|%|D/Sus' -r='enable' -o='./output' -nh -ndl -nfn -nnl -nb

../../fancychords --cli_in='Dsus2|x,1,3,3,2,1|x,1,3,4,2,1|%|%|%|D/Sus' -c -r='enable' -o='./output' -ndl -nfn -nnl -nb

../../fancychords --cli_in='Dsus3|x,1,3,3,2,1|x,1,3,4,2,1|%|%|%|D/Sus' -c -r='enable' -o='./output' -nfn -nnl -nb

../../fancychords --cli_in='Dsus4|x,1,3,3,2,1|x,1,3,4,2,1|%|%|%|D/Sus' -c -r='enable' -o='./output' -nnl -nb

../../fancychords --cli_in='Dsus5|x,1,3,3,2,1|x,1,3,4,2,1|%|%|%|D/Sus' -c -r='enable' -o='./output' -nb

../../fancychords --cli_in='Dsus6|x,1,3,3,2,1|x,1,3,4,2,1|%|%|%|D/Sus' -c -r='enable' -o='./output'

../../fancychords --cli_in='Dsus7|x,1,3,3,2,1|x,1,3,4,2,1|%|%|x,R,5,R,b3,5|D/Sus' -c -r='enable' -o='./output' -ft

../../fancychords --cli_in="Dsus8|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,1,3,4,2,1|D/Sus" -c -r="enable" -o="./output" -ft -rd


# --cli_in & font tests

../../fancychords --cli_in='E1UbuN|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd

../../fancychords --cli_in='E2UbuB|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -fw='bold'

../../fancychords --cli_in='E3DejN|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -ff='DejaVu Sans Mono'

../../fancychords --cli_in='E4DejB|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -fw='bold' -ff='DejaVu Sans Mono'

../../fancychords --cli_in='E5LibN|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -ff='Liberation Mono'

../../fancychords --cli_in='E6LibB|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -fw='bold' -ff='Liberation Mono'

../../fancychords --cli_in='E7CouN|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -ff='Courier New'

../../fancychords --cli_in='E8CouB|x,1,3,3,2,1|x,1,3,4,2,1|x,R,5,R,b3,5|%|x,R,5,R,b3,5|Eb/Sus' -c -r='enable' -o='./output' -ft -rd -fw='bold' -ff='Courier New'


deactivate
echo 'Job Done!'
