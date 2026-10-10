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
import os
import shutil


def newname(target_chord_dir,
            source_chord_fullname,
            source_chord_ext,
            source_chord_namesplit,
            overwrite):
    """
    Find a new name for chord if overwrite flag is false:
    ie, if Gmin.v02.svg exists then another Gmin would go from
    '../dirout/Major/Gmin.v02.svg' to '../dirout/Major/Gmin.v03.svg'
    
    target_chord_dir: String, example '../dirout/Major'
    source_chord_fullname: String, example 'Gmin.v02.svg'
    source_chord_ext: String, example '.svg'
    source_chord_namesplit: Tuple, example ('Gmin', 2)
    overwrite: Boolean, if overwrite files
    
    return target_chord_path: '../dirout/Major/Gmin.v03.svg'
    """
    # source_chord_name: 'Gmin', source_chord_version: 2
    source_chord_name, source_chord_version = source_chord_namesplit
    # target_chord_path: '../dirout/Major/Gmin.v02.svg'
    target_chord_path = os.path.join(target_chord_dir, source_chord_fullname)
    if not overwrite:
        if os.path.exists(target_chord_path):
            # target_chord_version = 2 + 1 = 3
            target_chord_version = source_chord_version + 1
            # target_chord_namesplit: ('Gmin', 3)
            target_chord_namesplit = (source_chord_name, target_chord_version)
            # target_chord_fullname: 'Gmin.v03.svg' 
            target_chord_fullname = source_chord_name + '.v' + str(target_chord_version).zfill(2) + source_chord_ext
            # recursion to find a number which is not already taken
            # that is if a 'Gmin.v03.svg' exist then go on and check a 'Gmin.v04.svg'
            target_chord_path = newname(
                  target_chord_dir
                , target_chord_fullname
                , source_chord_ext
                , target_chord_namesplit
                , overwrite
                )      
    return target_chord_path


def merge_chord_tree(dir_source, dir_target, file_exts, overwrite=False):
    '''
    merge two chords dirs
    
    dir_source: String, directory source to copy from
    dir_target: String, directory target to copy to
    file_exts: Tuple of strings, allowed extension for files to process, ie ('.svg', '.png'),
               use ('.xyz',) for singleton tuple
    overwrite: Boolean, if overwrite files
    
    return explicative message
    '''
    # list with all parameters needed for merging (see below)
    mylist_toprocess = []
    # os normalize dir paths
    dir_source = os.path.normpath(dir_source)
    dir_target = os.path.normpath(dir_target)
    header = '\n=====================  Merging Chords Trees  ========================='
    print(header)
    option_summary = ('{:<10} {} {:<10} {}').format('dir_source:', dir_source, '\ndir_target:', dir_target)
    print(option_summary)
    # os.walk returns a generator, that creates a tuple of values 
    # (actual path, directories in actual path, files in actual path).
    for oswalk_triplet in os.walk(dir_source):
        act_path = oswalk_triplet[0]
        files_in_act_path = oswalk_triplet[2]
        # process only certain filetype
        for myext in file_exts:
            for myfile in files_in_act_path:
                if myfile.endswith(myext):
                    # splitext split the pathname path into a pair (root, ext)
                    # Gmin.v02.svg -> ('Gmin.v02', 'svg')
                    (fname, fext) = os.path.splitext(myfile)
                    # if there is one or more dot in fname (Gmin.v02)
                    if fname.count('.') >= 1:
                        # Gmin.v02 -> ('Gmin', 'v02')
                        (chord_name, chord_postfix) = fname.split('.', 1)
                        # 'v02' -> 2
                        chord_version = int(chord_postfix[-1])
                    else:
                        (chord_name, chord_version) = (fname, 1)
                    # meaningful names
                    source_chord_fullname = myfile # 'Gmin.v02.svg'
                    source_chord_dir = act_path # '../dirin/Major'
                    # '../dirin/Major/Gmin.v02.svg'
                    source_chord_path = os.path.join(act_path, myfile)
                    # '../dirout/Major'
                    target_chord_dir = os.path.normpath(act_path.replace(dir_source, dir_target))
                    # '.svg'
                    source_chord_ext = fext
                    # ('Gmin', 2)
                    source_chord_namesplit = (chord_name, chord_version)
                    '''
                    mylist_toprocess = [
                                         (
                                         '../dirin/Major/Gmin.v02.svg'
                                         , '../dirin/Major'
                                         , '../dirout/Major'
                                         , 'Gmin.v02.svg'
                                         , '.svg'
                                         , ('Gmin', 2)
                                         )
                                         , (... 
                                       ]
                    '''
                    # append all infos to mylist_toprocess
                    mylist_toprocess.append(
                        (
                              source_chord_path
                            , source_chord_dir
                            , target_chord_dir
                            , source_chord_fullname
                            , source_chord_ext
                            , source_chord_namesplit
                        )
                    )
    msg_str = ''
    for elem in mylist_toprocess:
        # print '\n', elem
        source_chord_path = elem[0]
        target_chord_dir = elem[2]
        source_chord_fullname = elem[3]
        source_chord_ext = elem[4]
        source_chord_namesplit = elem[5]
        # use newname function to get correct target_chord_path
        target_chord_path = newname(
              target_chord_dir
            , source_chord_fullname
            , source_chord_ext
            , source_chord_namesplit
            , overwrite
            )
        body = ('{} {:<35} {} {}').format('Copying:', source_chord_path, ' --> ', target_chord_path)
        msg_str += '\n' + body
        print(body)
        # check if target_chord_dir exist otherwise, create it
        if not os.path.exists(target_chord_dir): os.makedirs(target_chord_dir)
        # do the copy
        shutil.copy(source_chord_path, target_chord_path)
    return header + '\n' + option_summary + msg_str


if __name__ == "__main__":
    
    # testing this functions
    
    from libs import htmlreport
    
    # --- functions parameters ---    
    file_exts = ('.svg', '.png')        # allowed extension for files to process, use ('.xyz',) for singleton tuple
    dir_source = '../dirin'             # directory source to copy from
    dir_target = '../dirout'            # directory target to copy to
    ncols = 4                           # number of columns for the gallery
    thumb_width = '200.0px'             # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    
    merge_chord_tree(dir_source, dir_target, file_exts, overwrite=False)
    htmlreport.generate_htmlreport(dir_target, file_exts, ncols, thumb_width)
    
    footer = "======================================================================"
    print(footer)
    # print aa + '\n' + bb + '\n' + footer
