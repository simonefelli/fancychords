#!/bin/bash
# run from this script dir, so relative paths work wherever the script is called from
cd "$(dirname "$0")" || exit 1
# absolute path of the tests dir, used by the "absolute path" test cases
TESTS_DIR="$(cd .. && pwd)"
# activate the python virtualenv if present (override with: VENV=/my/venv ./script.sh)
VENV="${VENV:-/home/simone/MyApps/Dev/myvenv}"
if [ -f "$VENV/bin/activate" ]; then source "$VENV/bin/activate"; fi
python3 ../../fancychords.py --file_in='../crds_test_files/caged_chords.txt' -r='enable' -cf='../json_cfg_tests_files/config_caged_chords.json' -o='./dirout/chords'
# deactivate only if a virtualenv was activated
if type deactivate >/dev/null 2>&1; then deactivate; fi
echo 'Job Done!'
