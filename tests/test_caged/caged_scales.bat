@echo off


REM ========= S&R =========
REM python3 -> python
REM " -> "
REM % -> %%
REM # -- -> REM --
REM =======================

python ../../fancyscales.py "../scls_tests_files/caged_scales.txt" -r="enable" -cf="../json_cfg_tests_files/config_scales.json" -o="./dirout/scales"

python ../../fancyscales.py "../scls_tests_files/scales-all-neck.txt" -r="enable" -cf="../json_cfg_tests_files/config_scales_all_neck.json" -o="./dirout/scales_all_neck"

python ../../fancyscales.py "../scls_tests_files/caged_scales.txt" -r="enable" -cf="../json_cfg_tests_files/config_scales_all_neck_padded.json" -o="./dirout/scales_all_neck"


echo Job Done!
