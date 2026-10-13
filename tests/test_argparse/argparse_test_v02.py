# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Simone Felli
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


import argparse

parser = argparse.ArgumentParser()


# create a mutually exclusive group, one option is required
excl_group = parser.add_mutually_exclusive_group(required=True)
excl_group.add_argument(
    '--cli_in'
    , action='store'
    , dest='onechord_str'
    )
excl_group.add_argument(
    '--file_in'
    , action='store'
    , dest='input_crdf'
    )


# optional config file argument
parser.add_argument(
      '--config_file'
    , type=argparse.FileType('r')
    , help='input json file path'
        )


# define 3 subparsers. One for login, one for register and one for array
# required=True only fot python >= 3.7
subparser = parser.add_subparsers(dest='command')

login = subparser.add_parser('login')
# -- login arguments
login.add_argument('--username', type=str, required=True)
login.add_argument('--password', type=str, required=True)

register = subparser.add_parser('register')
# -- register arguments
register.add_argument('--firstname', type=str, required=True)
register.add_argument('--lastname', type=str, required=True)

myarray = subparser.add_parser('array')
# -- array argument
myarray.add_argument(nargs='*', dest='myarray', type=str)



# args = parser.parse_args()

# multiple tests

'''
args = parser.parse_args(
    [  '--cli_in', 'xxxxx'
     , 'login'     
     , '--username', 'hansolo'
     , '--password', 'falcon'
     ]
    )
# python3 ./test_argparse.py -cli_in='xxxxx' login --username='hansolo' --password='falcon' ->
#    Logging in with username: hansolo and password: falcon


args = parser.parse_args(
    [  '--cli_in', 'xxxxx'
     , 'register'     
     , '--firstname', 'Han'
     , '--lastname', 'Solo'
     ]
    )
# python3 ./test_argparse.py -cli_in='xxxxx' register --firstname='Han' --lastname='Solo' ->
#    Creating firstname/lastname:  Han Solo


args = parser.parse_args(
    [  '--cli_in', 'xxxxx'
     , 'register'
     , '--username', 'hansolo'  
     , '--firstname', 'Han'
     , '--lastname', 'Solo'
     ]
    )
# python3 ./test_argparse.py -cli_in='xxxxx' register --username='hansolo' --firstname='Han' --lastname='Solo' ->
#    error: unrecognized arguments: --username=hansolo


args = parser.parse_args(
    [  '--cli_in', 'xxxxx'
     , 'array', '1,3,2,x', 'R,b7,5,3'
     ]
    )
# python3 ./test_argparse.py -cli_in='xxxxx' array '1,3,2,x' 'R,b7,5,3' -> 
#    myarray:  ['1,3,2,x', 'R,b7,5,3,', '']
'''

args = parser.parse_args(
    [  '--cli_in', './dummytextfile.txt'
     , '--config_file', '../json_cfg_tests_files/argparse_config.json'     
     , 'login'
     , '--username', 'hansolo'
     , '--password', 'falcon'
     ]
    )
# python3 ./test_argparse.py --cli_in=./dummytextfile.txt --config_file=./tests_files/config.json login .... ->
#    { ... }  Logging in with username: hansolo and password: falcon



print(args)

if args.config_file:
    with args.config_file as config_file:
        print(config_file.read())

if args.command == 'login':
    print('Logging in with username:', args.username, 'and password:', args.password)
elif args.command == 'register':
    print('Creating firstname/lastname:', args.firstname, args.lastname)
elif args.command == 'array':
    print('myarray: ', args.myarray)

