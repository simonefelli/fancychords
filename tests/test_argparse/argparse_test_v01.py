# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Simone Felli
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

# standard library imports
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
          description='Simple chords drawing program'
        , prog='fancychords'        
        , epilog='Have fun playing guitar!'
        )
    
    # test optional argument
    parser.add_argument(
        '-o'
        , action='store'
        , dest='dir_output'
        , default='./dirout'
        )

    # define two subparsers. One for cli and one for config file
    # required=True only fot python >= 3.7
    subparser = parser.add_subparsers(dest='command', required=True)
    cli = subparser.add_parser('cli')
    cfg = subparser.add_parser('cfg')
    
    
    # -- cli arguments --
    
    # cli positional FileType argument (required)
    cli.add_argument(
        'input_crdf'
        , type=argparse.FileType('r')
        , help='input chords file path'
        )
    
    
    # -- cfg arguments --
    
    # cfg positional FileType argument (required)
    cfg.add_argument(
        'json_file'
        , type=argparse.FileType('r')
        , help='input json file path'
        )
    
    
    # -- main call of the parser --
    
    crdf =  '../crds_test_files/argparse_caged.csv'
    jsonf = '../json_cfg_tests_files/argparse_config.json'
    


    args = parser.parse_args([
         '-o', './dummytextfile.txt'       
        , 'cfg', crdf,
        ])
    
    '''
    
    args = parser.parse_args([
        'cli', jsonf
        ])
        
    '''
    
    # cli subparsers case
    
    if args.command == 'cli':
        with args.input_crdf as input_crdf:
            print(input_crdf.read())
            
    # cfg subparsers case
    
    elif args.command == 'cfg':
        with args.json_file as json_file:
            print(json_file.read())
    
    print(args)