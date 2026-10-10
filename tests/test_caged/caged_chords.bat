@echo off


REM ========= S&R =========
REM python3 -> python
REM ' -> "
REM % -> %%
REM # -- -> REM --
REM =======================

python ../../fancychords.py --file_in="../crds_test_files/caged_chords.txt" -r="enable" -cf="../json_cfg_tests_files/config_caged_chords.json" -o="./dirout/chords"


echo Job Done!
