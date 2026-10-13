@echo off

REM run from this script dir, so relative paths work wherever the script is called from
cd /d "%~dp0"
REM absolute path of the tests dir, used by the "absolute path" test cases
set "TESTS_DIR=%~dp0.."

REM ========= S&R =========
REM python3 -> python
REM ' -> "
REM % -> %%
REM # -- -> REM --
REM =======================

REM --file_in and check absolute/relative paths

python ../../fancyscales.py ../scls_tests_files/scale-list.txt -c -rd -r="enable" -o="./output/major"

python ../../fancyscales.py ../scls_tests_files/arpeggios-list.txt -o="%TESTS_DIR%\\test_fancyscales\\output\\arpeggios" -cf="%TESTS_DIR%\\json_cfg_tests_files\\config_scales.json"

python ../../fancyscales.py ../scls_tests_files/caged_scales.txt -o="./output/caged" -cf="../json_cfg_tests_files/config_scales.json"

python ../../fancyscales.py ../scls_tests_files/scales-all-neck.txt -o="./output/all-neck" -cf="../json_cfg_tests_files/config_scales_all_neck.json"

python ../../fancyscales.py ../scls_tests_files/caged_scales.txt -o="./output/all-neck-pad" -cf="../json_cfg_tests_files/config_scales_all_neck_padded.json"

echo Job Done!
