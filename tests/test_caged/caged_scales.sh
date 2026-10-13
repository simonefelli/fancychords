#!/bin/bash
# run from this script dir, so relative paths work wherever the script is called from
cd "$(dirname "$0")" || exit 1
# absolute path of the tests dir, used by the "absolute path" test cases
TESTS_DIR="$(cd .. && pwd)"
# activate a python virtualenv if present: by default .venv in the repository
# root (python3 -m venv .venv), or any other one with: VENV=/my/venv ./script.sh
# (without a virtualenv the system python3 is used)
VENV="${VENV:-../../.venv}"
if [ -f "$VENV/bin/activate" ]; then source "$VENV/bin/activate"; fi

python3 ../../fancyscales.py '../scls_tests_files/caged_scales.txt' -r='enable' -cf='../json_cfg_tests_files/config_scales.json' -o='./dirout/scales'

python3 ../../fancyscales.py '../scls_tests_files/scales-all-neck.txt' -r='enable' -cf='../json_cfg_tests_files/config_scales_all_neck.json' -o='./dirout/scales_all_neck'

python3 ../../fancyscales.py '../scls_tests_files/caged_scales.txt' -r='enable' -cf='../json_cfg_tests_files/config_scales_all_neck_padded.json' -o='./dirout/scales_all_neck'

# deactivate only if a virtualenv was activated
if type deactivate >/dev/null 2>&1; then deactivate; fi
echo 'Job Done!'