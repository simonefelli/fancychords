import json
# local application imports
from libs import global_utilities

json_file = '../json_cfg_tests_files/config_scales.json'
with open(json_file, 'r') as jsonfile: db_dict_jdump = json.load(jsonfile)

global_utilities.fill_jdump(db_dict_jdump, 1.40, 22.00, None)

print(db_dict_jdump)

