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


"""
convert_svg2png: convert svg chord images to png images.

convert_svg2png() uses the cairosvg python library (default, used by
fancychords -c). convert_external_svg2png() can call an external program
instead (ie Inkscape or ImageMagick), it is kept for manual use.
"""

# standard library imports
import os
import urllib.parse
import cairosvg
import subprocess
from libs import global_utilities


def convert_svg2png(svg_dir, png_dir, chord_filenames_list):
    """
    batch convert svg chords to png chords using python cairosvg lib.

    svg_dir: String, dir (and sub-dirs) containing svg images to process, ie: '.../dirout/G/Major'
    png_dir: String, placement dir for png images, ie: '.../dirout/G/Major/png'
    chord_filenames_list: List, list with filenames to process
    
    return explicative message, png_file_path_list
    """
    svg_file_list = []
    png_file_path_list = []
    # for matching os.listdir with chord_filenames_list we need to sanitize every name
    # in chord_filenames_list: [Cm(maj7), ...] -> [Cmmaj7, ...]
    chord_filenames_list = [global_utilities.sanitize_str(filename) for filename in chord_filenames_list]
    
    for fl in os.listdir(svg_dir):
        if fl.endswith('svg'):
            svg_file_list.append(fl)
    msg_str = ''
    for svg_file in svg_file_list:
        
        # splitext: 'pychords.svg' -> ('pychords', '.svg')
        actual_filename = os.path.splitext(svg_file)[0]
        
        # check if chord in filesystem is in our "to process" list
        # otherwise skip it
        if actual_filename in chord_filenames_list:
            
            # if png dir does not exist, create it
            if not os.path.isdir(png_dir): os.makedirs(png_dir)
            
            # cairosvg.svg2png seem to work only with relative files (on Windows?)
            svg_file_rel_path = os.path.relpath(svg_dir + svg_file)
            png_file_rel_path = os.path.relpath(png_dir + actual_filename + '.png')
            
            svg_file_path = os.path.normpath(svg_file_rel_path)
            png_file_path = os.path.normpath(png_file_rel_path)
            
            # print(svg_file_path)
            urlquote_svg_file_path = urllib.parse.quote(svg_file_path)
            # print(urlquote_svg_file_path)
            
            # cairosvg.svg2png(scale=0.5, url=urllib.parse.quote(svg_file_path), write_to=png_file_path)
            cairosvg.svg2png(url=urlquote_svg_file_path, write_to=png_file_path)
            
            png_file_path_list.append(png_file_path)

            print_label = "* " + actual_filename
                
            # {":" format_spec} Padding and aligning strings
            # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
            # and XX is the width for specific value.
            body = '{:<22} {}'.format(
                        print_label,
                        svg_file_path + '\n'
                    ) + '{:>22} {}'.format(
                        ' --> ',
                        png_file_path
                        )                                   
            print(body)
            msg_str += '\n' + body
   
    return msg_str, png_file_path_list


def convert_external_svg2png(svg_dir, png_dir, convert_cmd, chord_filenames_list):
    """
    batch convert svg chords to png chords using an external cli program.
    Tested with Inkscape and ImageMagick convert

    svg_dir: String, dir (and sub-dirs) containing svg images to process, ie: '.../dirout/G/Major'
    png_dir: String, placement dir for png images, ie: '.../dirout/G/Major/png'
    convert_cmd: Tuple with command line parts
        (
          cmd_bin: String, path binary for converter
        , cmd_option: String, cli options
        , cmd_svg: String, pre svg-file path option
        , cmd_png: String, pre png-file path option
        )
        ie: mybin --noidea -input="./mysvg.svg" -out="./mysvg.png"
        convert_cmd = ('mybin', ' --noidea', ' -input=', ' -out=')
    chord_filenames_list: List, list with filenames to process
    
    return explicative message, png_file_path_list
    """
    svg_file_list = []
    png_file_path_list = []
    for fl in os.listdir(svg_dir):
        if fl.endswith('svg'):
            svg_file_list.append(fl)
    msg_str = ''
    for svg_file in svg_file_list:
        
        # splitext: 'pychords.svg' -> ('pychords', '.svg')
        actual_filename = os.path.splitext(svg_file)[0]
        
        # check if chord in filesystem is in our "to process" list
        # otherwise skip it
        if actual_filename in chord_filenames_list:
            
            # if png dir does not exist, create it
            if not os.path.isdir(png_dir): os.makedirs(png_dir)
            
            # first get relative paths then turn them in absolute
            svg_file_rel_path = os.path.relpath(svg_dir + svg_file)
            png_file_rel_path = os.path.relpath(png_dir + actual_filename + '.png')
            
            svg_file_path = os.path.normpath(svg_file_rel_path)
            png_file_path = os.path.normpath(png_file_rel_path)
            
            cmd_bin, cmd_option, cmd_svg, cmd_png = convert_cmd
            
            mycmd = cmd_bin + cmd_option + cmd_svg + \
                    '"' + svg_file_path + '"' + cmd_png + '"' + png_file_path + '"'
            # print(mycmd)
            
            p = subprocess.Popen(mycmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            poutput, perrors = p.communicate()
            # print(poutput, perrors)
            png_file_path_list.append(png_file_path)
            
            print_label = "* " + actual_filename
            poutput_label = '(' + str(poutput[:50]) + '...)' if poutput else ''
            perrors_label = '(' + str(perrors[:50]) + '...)' if perrors else ''

            # {":" format_spec} Padding and aligning strings
            # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
            # and XX is the width for specific value.
            body = '{:<22} {}'.format(
                        print_label,
                        svg_file_path + '\n'
                    ) + '{:>22} {} {} {}'.format(
                        ' --> ',
                        png_file_path,
                        poutput_label,
                        perrors_label
                        )                                   
            print(body)
            msg_str += '\n' + body
   
    return msg_str, png_file_path_list



if __name__ == "__main__":
    
    
    # --- testing convert_svg2png function ---
    
    svg_dir = '../dirin/svg/'       # dir (and sub-dirs) containing svg images to process
                                    # ie: '.../dirout/G/Major/' 
    # svg_dir = 'C:\\Users\\sfelli\\simo\\dev\\python\\py3\\pychords\\app\\dirin\\svg\\'

    png_dir = '../dirin/svg/png/'   # placement dir for png images
                                    # ie: '.../dirout/G/Major/png/'
    # png_dir = 'C:\\Users\\sfelli\\simo\\dev\\python\\py3\\pychords\\app\\dirin\\svg\\png\\' 

    chord_filenames_list = ['Am7', 'A#m7', 'Dm7']   # list with filenames to process
    
    header = "Converting SVG Chords to PNG using internals\n============================================"
    print(header)    
    
    msg_str, png_file_path_list = convert_svg2png(svg_dir, png_dir, chord_filenames_list)
    # print(msg_str)
    
    # print(png_file_path_list)
    
    
    # --- testing convert_external_svg2png function ---
                                  
    chord_filenames_list = ['G', 'T', 'arrows']   # list with filenames to process
    
    header = "\nConverting SVG Chords to PNG using external\n==========================================="
    print(header)
    
    
    # Inkscape:
    # inkscape --export-area-page --export-type="png" "./G.svg" --export-filename="./png/G.png"
    # '/home/simone/MyApps/Graphics/inkscape/Inkscape-x86_64.AppImage' for Appimage
    # 'inkscape.exe' for win
    convert_cmd = (
          '/home/simone/MyApps/Graphics/inkscape/Inkscape-x86_64.AppImage'
        , ' --export-area-page'
        , ' --export-type="png" '
        , ' --export-filename='
        )
    
    '''
    # Imagemagick Convert:
    # convert -background None "./arrows.svg" "./png/arrows.png"
    convert_cmd = (
          'convert'
        , ' -background None'
        , ' '
        , ' '
        )   
    '''
    
    msg_str, png_file_path_list = convert_external_svg2png(svg_dir, png_dir, convert_cmd, chord_filenames_list)
    # print(msg_str)
    
    # print(png_file_path_list)
    
