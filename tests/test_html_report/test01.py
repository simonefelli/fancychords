import os
import urllib.request

dir_output = '../dirout'

images_file_path_list = [
    '../dirout/SI11.svg', 
    '../dirout/DOX.svg', 
    '../dirout/aa/DOY.svg', 
    '../dirout/aa/DOW.svg', 
    '../dirout/aa/ZAP.svg', 
    '../dirout/bb/XXX.svg', 
    '../dirout/bb/YYY.svg', 
    '../dirout/bb/ZZZ.svg', 
    '../dirout/aa/cc/DO.svg', 
    '../dirout/aa/dd/DO.v02.svg', 
    '../dirout/aa/ee/DO_RE.svg', 
    '../dirout/bb/ff/DO7.svg', 
    '../dirout/bb/gg/DO7+.svg', 
    '../dirout/bb/hh/DO9.svg', 
    '../dirout/bb/ii/RE#m.svg', 
    '../dirout/bb/ll/RE#dib7.svg', 
    '../dirout/bb/ii/qq/SOL.svg', 
    '../dirout/bb/ii/ww/SOL7.svg', 
    '../dirout/bb/ll/kk/oo/SOL#dib7(no5)_FA#.svg', 
    '../dirout/bb/ll/kk/pp/LA.svg',
    '../dirout/png/SI11.png', 
    '../dirout/png/DOX.png', 
    '../dirout/bb/png/ZZZ.png', 
    '../dirout/bb/png/XXX.png', 
    '../dirout/bb/png/YYY.png', 
    '../dirout/bb/ii/png/RE#m.png', 
    '../dirout/bb/ii/ww/png/SOL7.png', 
    '../dirout/bb/ii/qq/png/SOL.png', 
    '../dirout/bb/hh/png/DO9.png', 
    '../dirout/bb/ll/png/RE#dib7.png', 
    '../dirout/bb/ll/kk/pp/png/LA.png', 
    '../dirout/bb/ll/kk/oo/png/SOL#dib7(no5)_FA#.png', 
    '../dirout/bb/gg/png/DO7+.png', 
    '../dirout/bb/ff/png/DO7.png', 
    '../dirout/aa/png/ZAP.png', 
    '../dirout/aa/png/DOW.png', 
    '../dirout/aa/png/DOY.png', 
    '../dirout/aa/dd/png/DO.v02.png', 
    '../dirout/aa/cc/png/DO.png', 
    '../dirout/aa/ee/png/DO_RE.png'
    ]

images_dir_list = []
images_dir_files_dict = {}

for image_path in images_file_path_list:
    image_dir= os.path.dirname(image_path)
    images_dir_list.append(image_dir)
    if image_dir in images_dir_files_dict:
        images_dir_files_dict[image_dir].append(image_path)
    else:
        images_dir_files_dict[image_dir] = [image_path]

images_grouped_dir_list= list(set(images_dir_list))

print(images_grouped_dir_list)
print(images_dir_files_dict)


images_dir_childirs_dict = {}

for pdir in images_grouped_dir_list:
    
    cdirs = [name for name in os.listdir(pdir) if os.path.isdir(os.path.join(pdir, name))]  
    for cdir in cdirs:
        if os.path.join(pdir, cdir) in images_grouped_dir_list:
            if pdir in images_dir_childirs_dict:
                images_dir_childirs_dict[pdir].append(cdir)
            else:
                images_dir_childirs_dict[pdir] = [cdir]
        
print(images_dir_childirs_dict)


def smart_htmlreport(dir_output, ncols, thumb_width):
    
    html_file_name = 'report.html'
    
    # just for keeping track of these numbers for statistics
    n_scanned_dirs =  len(images_grouped_dir_list)
    n_scanned_files = len(images_file_path_list)
    
    myexts_dict = {}
    for image_file in images_file_path_list:
        file_extension = os.path.splitext(image_file)[1]
        if file_extension in myexts_dict:
            myexts_dict[file_extension] += 1
        else:
            myexts_dict[file_extension] = 1
    
    # os normalize dirs paths
    dir_output = os.path.normpath(dir_output) 
    
    # check if dir_output exist
    if os.path.isdir(dir_output):

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
                
        for rootpath in images_grouped_dir_list:
                
            # remove from root path initial base dir
            # ie: '../dirout/G/Minor/....' -> 'G/Minor/....'
            breadcrumb = rootpath.replace(dir_output, '', 1)
            
            dirs = images_dir_childirs_dict[rootpath] if rootpath in images_dir_childirs_dict else []
            files = images_dir_files_dict[rootpath] if rootpath in images_dir_files_dict else []
            
            # sorting names
            sorted_dirs = sorted(dirs)
            n_dirs = len(sorted_dirs)
            sorted_files = sorted(files)
            n_files = len(files)
            
            # create index.html and populate it
            indexfile = open(os.path.join(rootpath, html_file_name), mode='w')
            indexfile.write(header)
            infos = '\n      <p>Number of subdirs: ' + str(n_dirs)  + '<br>' + \
                    '\n         Number of images: '  + str(n_files) + '</p>\n'                
            if breadcrumb:
                subheader = '    <h2>' + breadcrumb + '</h2>            ' + infos + \
                            '      ' + link_to_back + '\n'
            else:
                subheader = '    <h2>Root Dir</h2>            ' + infos
            indexfile.write(subheader)
            
            if sorted_dirs:
                indexfile.write('    <h3>Subdirs</h3>\n    <ul>\n')
                for actdir in sorted_dirs:
                    dir_link = urllib.request.pathname2url(os.path.join(actdir, html_file_name))
                    indexfile.write('      <li><a href="' + dir_link + '">' + actdir + '</a></li>\n')
                indexfile.write('    </ul>')
            
            if sorted_files:
                nfiles = len(sorted_files)
                files = [file.replace(rootpath, '.', 1) for file in sorted_files]
                table_list = [files[i:i + ncols] for i in range(0, nfiles, ncols)]
                tr_start = '        <tr>\n          <td>'
                td_elem = '</td>\n          <td>'
                tr_end = '</td>\n        </tr>\n'
                indexfile.write(body)
                for row in table_list:
                    links = ['<img alt="' + elem + '" title="' + elem + \
                             thumb_width_str + \
                             '" src="' + urllib.request.pathname2url(elem) + '">' for elem in row]
                    indexfile.write(tr_start)
                    indexfile.write(td_elem.join(links))
                    indexfile.write(tr_end)
                indexfile.write('      </tbody>\n    </table>\n')
            
            indexfile.write(footer)
        
            indexfile.close
        # useful messages
        header = 'Generating HtmlReport\n====================='
        # print('\n' + header)
        option_summary = ('{} {:<4} {} {:<4}').format(
              'Number of scanned_dirs: ',   str(n_scanned_dirs) 
            , '\nNumber of scanned_files:', str(n_scanned_files)
            )    
        # print(option_summary)
        msg_str = ''
        for elem in myexts_dict:
            myext_num = myexts_dict[elem]
            if myext_num > 0:
                body = 'Number of ' + elem + ' files:    ' + str(myext_num)
                # print(body)
                msg_str += '\n' + body
        msg_str = header + '\n' + option_summary + msg_str
        
        print(msg_str)
        
    # if dir_output do not exist do nothing and report it
    else:
        msg_str = 'Error: ' + dir_output + ' do not exist'
        print(msg_str)


smart_htmlreport(dir_output, 4, '200.0px')
