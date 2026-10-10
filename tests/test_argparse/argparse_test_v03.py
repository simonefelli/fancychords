
import argparse

default_params = {
      'dir_output': './dirout'
    , 'horiz': False
    , 'lntk': 3.04
    , 'fretb_format': {
              '*': (1.0, 'black', 'black', 'none', '3', 'white', 
                  'bold', 'Ubuntu Mono Legacy', False, False)
            , 'r': (1.0, 'lightgrey', 'black', 'none', '5', 'black', 
                    'bold', 'Ubuntu Mono Legacy', False, False)
        }
    }

def param_check(db_dict_jdump, args_param, param_name, param_section):
    
    if db_dict_jdump:
        j_param = db_dict_jdump[param_section].get(param_name)
        if j_param is not None: 
            default_params[param_name] = j_param

    if args_param is not None:
        default_params[param_name] = args_param
    
    return default_params[param_name]


if __name__ == "__main__":

    program_version = '0.3'
    program_author = 'Simone Felli'
    
    # parser declaration
    parser = argparse.ArgumentParser(
          description='Simple chords drawing program'
        , prog='fancychords'        
        , epilog='Have fun playing guitar!'
        )

    # --- optional arguments ---
    parser.add_argument(
        '-cf', '--config_file'
        , dest='json_file'
        , help='input config json file path'
        )
    parser.add_argument(
        '-o', '--output-dir'
        , action='store'
        , dest='dir_output'
        , default=None
        , help='output dir for images, default is \'%(default)s\''
        )
    parser.add_argument(
        '-ho', '--horizontal'
        , action="store_true"
        , dest='horiz'
        , default=None
        , help='draw chords horizontally, default is \'%(default)s\''
        )
    parser.add_argument(
        '-l', '--lntk'
        , action='store'
        , dest='lntk'
        , type=float
        , default=None
        , help='grid line tickness, default is \'%(default)s\''
        )

    # -- main call of the parser --

    try:
        
        # args = parser.parse_args()        
        # args = parser.parse_args(['--output-dir', '../clinewdir', '--horizontal'])
        # args = parser.parse_args(['--config_file', './argparse_config.json'])        
        # args = parser.parse_args(['--output-dir', '../clinewdir', '--config_file', '../json_cfg_tests_files/argparse_config.json'])
        # args = parser.parse_args(['--output-dir', '../clinewdir'])
        args = parser.parse_args(['--config_file', '../json_cfg_tests_files/argparse_config.json', '--lntk', '5'])   

        
        if args:
            
            db_dict_jdump = {}
            
            if args.json_file:
                import json
                json_file = args.json_file
                with open(json_file, 'r') as jsonfile:
                    db_dict_jdump = json.load(jsonfile)

        dir_output = param_check(db_dict_jdump, args.dir_output, 'dir_output', 'i/o')
        horiz = param_check(db_dict_jdump, args.horiz, 'horiz', 'flags')
        lntk = param_check(db_dict_jdump, args.lntk, 'lntk', 'parameters')
        fretb_format = param_check(db_dict_jdump, None, 'fretb_format', 'generic_formats')


    except Exception as e:
        print(e)


    print(args)
    print('- dir_output: ', dir_output)
    print('- horiz: ', horiz)
    print('- lntk: ', lntk)
    print('- fretb_format: ', fretb_format)
