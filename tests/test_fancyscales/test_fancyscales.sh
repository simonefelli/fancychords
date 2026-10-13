#!/bin/bash
# run from this script dir, so relative paths work wherever the script is called from
cd "$(dirname "$0")" || exit 1
# absolute path of the tests dir, used by the "absolute path" test cases
TESTS_DIR="$(cd .. && pwd)"
# activate the python virtualenv if present (override with: VENV=/my/venv ./script.sh)
VENV="${VENV:-/home/simone/MyApps/Dev/myvenv}"
if [ -f "$VENV/bin/activate" ]; then source "$VENV/bin/activate"; fi

python3 ../../fancyscales.py ../scls_tests_files/scale-list.txt -c -rd -r='enable' -o='./output'

python3 ../../fancyscales.py ../scls_tests_files/arpeggios-list.txt -c -rd -r='enable' -o="$TESTS_DIR/test_fancyscales/output" -cf="$TESTS_DIR/json_cfg_tests_files/config_scales.json"

# deactivate only if a virtualenv was activated
if type deactivate >/dev/null 2>&1; then deactivate; fi
echo 'Job Done!'