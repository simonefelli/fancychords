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


"""
htmlreport: build an html gallery of the images in an output dir.

generate_htmlreport() writes a 'fcreport.html' file in dir_output and in
every subdir (up to 4 levels deep) with a table of thumbnails and links to
the subdirs, so all the chords can be browsed with a web browser.
"""


# standard library imports
import html
import os
import urllib.request


def generate_htmlreport(dir_output, file_exts, ncols, thumb_width):
    '''
    for a given directory (dir_output) process all file with certain extension (file_exts)
    and for every directory and subdirectory produce an html file (fcreport.html) with
    all images galleries. For security we limit deep of scanning to 5 subdirs
    
    dir_output: String, directory (and all its sub-dirs) to process
    file_exts: Tuple of strings, file extension names to process, ie ('.svg', '.png')
    ncols: Integer, number of columns for the gallery
    thumb_width: String, gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    
    return explicative message
    '''
    
    html_file_name = 'fcreport.html'
    
    # os normalize dirs paths
    dir_output = os.path.normpath(dir_output)
    
    # check if dir_output exist
    if os.path.isdir(dir_output):
        # just for keeping track of these numbers for statistics
        n_scanned_dirs = 0
        n_scanned_files = 0
        # dict with number of files by ext: {'.png': 12, '.svg': 12}
        # initialize with dict comprehension: {'.png': 0, '.svg': 0}
        myexts_dict = dict([(myext, 0) for myext in file_exts])
        # html header
        header = '''
 <!DOCTYPE html>
 <html>
   <head>
     <meta http-equiv="content-type" content="text/html; charset=UTF-8">
     <title>Chord Index</title>
   </head>
   <body>
     '''
        # html body
        body = '''
    <h3>Images</h3>
    <table style="margin-left: auto; margin-right: auto;" border="1">
      <tbody style="text-align:center;">
    '''
        # html footer
        footer = '    <p><em style="font-size: small;">Have fun playing guitar!</em></p>\n  </body>\n</html>'
        # html link to previous directory (relative)
        link_to_back = '<p><a href="../' + html_file_name + '"><strong>[Back To Parent]</strong></a></p>'
        if thumb_width:
            thumb_width_str = '" style="width: ' + thumb_width + ';'
        else:
            thumb_width_str = ''
        
        # os.walk returns a generator, that creates a tuple of values 
        # (root path, directories in root path, files in root path).
        for rootpath, dirs, files in os.walk(dir_output):
            # for security limit deep of os.walk to 4 subdirs.
            # path of rootpath relative to dir_output:
            # '../dirout' -> '.', '../dirout/G/Minor' -> 'G/Minor'
            rel_rootpath = os.path.relpath(rootpath, dir_output)
            # walk_deep: 0 for dir_output itself, 1 for its subdirs, ...
            # (computed from the relative path, so it is right both for
            # absolute and relative dir_output, ie '.', '../dirout', '/tmp/out')
            walk_deep = 0 if rel_rootpath == os.curdir else rel_rootpath.count(os.sep) + 1
            max_deep = 4
            # if max deep for subdirs is reached then empty dirs list.
            # note: dirs must be emptied in place (dirs[:] = []) because
            # os.walk reads this same list object to know where to go next:
            # a plain 'dirs = []' would not stop it from scanning deeper
            if walk_deep > max_deep - 1: dirs[:] = []
            # for breadcrumb remove from root path initial base dir
            # ie: '../dirout/G/Minor/....' -> '/G/Minor/....'
            breadcrumb = '' if rel_rootpath == os.curdir else os.sep + rel_rootpath
            # sorting names
            sorted_dirs = sorted(dirs)
            n_dirs = len(sorted_dirs)
            sorted_files = sorted(files)
            # filtering certain file types
            filtered_sorted_files = [fname for fname in sorted_files if fname.endswith(file_exts)]
            n_files = len(filtered_sorted_files)
            # for statistics
            n_scanned_dirs += n_dirs
            n_scanned_files += n_files
            # check how many files of a certain file type ('.png' or '.svg')
            for myext in file_exts:
                myexts_dict[myext] += len([fname for fname in filtered_sorted_files if fname.endswith(myext)])
            if sorted_dirs or sorted_files:
                # create index.html and populate it
                # html file is declared as UTF-8 in its header, so it must be
                # written as UTF-8 (Windows default encoding is different).
                # 'with' makes sure the file is closed when the block ends
                with open(os.path.join(rootpath, html_file_name), mode='w', encoding='utf-8') as indexfile:
                    indexfile.write(header)
                    infos = '\n      <p>Number of subdirs: ' + str(n_dirs) + '<br>' + \
                            '\n         Number of images: ' + str(n_files) + '</p>\n'                
                    if breadcrumb:
                        subheader = '    <h2>' + html.escape(breadcrumb) + '</h2>            ' + infos + \
                                    '      ' + link_to_back + '\n'
                    else:
                        subheader = '    <h2>Root Dir</h2>            ' + infos
                    indexfile.write(subheader)
                    if sorted_dirs:
                        indexfile.write('    <h3>Subdirs</h3>\n    <ul>\n')
                        for actdir in sorted_dirs:
                            dir_link = urllib.request.pathname2url(os.path.join(actdir, html_file_name))
                            indexfile.write('      <li><a href="' + dir_link + '">' + html.escape(actdir) + '</a></li>\n')
                        indexfile.write('    </ul>')

                    if filtered_sorted_files:
                        nfiles = len(filtered_sorted_files)
                        table_list = [filtered_sorted_files[i:i + ncols] for i in range(0, nfiles, ncols)]
                        tr_start = '        <tr>\n          <td>'
                        td_elem = '</td>\n          <td>'
                        tr_end = '</td>\n        </tr>\n'
                        indexfile.write(body)
                        for row in table_list:
                            # html.escape: a name with chars like '&' or '"' must not break the html
                            links = ['<img alt="' + html.escape(elem) + '" title="' + html.escape(elem) + \
                                     thumb_width_str + \
                                     '" src="' + urllib.request.pathname2url(elem) + '">' for elem in row]
                            indexfile.write(tr_start)
                            indexfile.write(td_elem.join(links))
                            indexfile.write(tr_end)
                        indexfile.write('      </tbody>\n    </table>\n')

                    indexfile.write(footer)
            
        # useful messages
        header = 'Generating HtmlReport\n====================='
        print('\n' + header)
        # {":" format_spec} Padding and aligning strings
        # {:XX} pad, {:>XX} pad and align right, {:<XX} pad and align left, {:^XX} pad and align center
        # and XX is the width for specific value.
        option_summary = ('{} {:<4} {} {:<4}').format(
              'Number of scanned_dirs: ', str(n_scanned_dirs) 
            , '\nNumber of scanned_files:', str(n_scanned_files)
            )    
        print(option_summary)
        msg_str = ''
        for elem in myexts_dict:
            myext_num = myexts_dict[elem]
            if myext_num > 0:
                body = 'Number of ' + elem + ' files:    ' + str(myext_num)
                print(body)
                msg_str += '\n' + body
        msg_str = header + '\n' + option_summary + msg_str
    
    # if dir_output do not exist, do nothing and report it
    else:
        msg_str = 'HtmlReport Error, path: ' + dir_output + ' do not exist'
        print(msg_str)
    
    return msg_str


if __name__ == "__main__":
    
    # testing this function
    
    dir_output = '../dirout'            # directory (and all its sub-dirs) to process
    
    file_exts = (".svg", ".png")        # allowed extension for files to process, use ('.xyz',) for singleton tuple
    ncols = 4                           # number of columns for the gallery
    thumb_width = '200.0px'             # gallery thumbs width in pixels or % ('200px' or '70%', None to disable)
    
    generate_htmlreport(dir_output, file_exts, ncols, thumb_width)    
