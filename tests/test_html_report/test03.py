import os

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


def smart_htmlreport(dir_output):
    
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
        
        for rootpath, dirs, files in os.walk(dir_output):
            # filtering certain file types
            for fname in files:
                if os.path.join(rootpath, fname) not in images_file_path_list: files.remove(fname)
            # filtering dirs
            for mydir in dirs:
                if os.path.join(rootpath, mydir) not in images_grouped_dir_list: dirs.remove(mydir)
            print(rootpath, dirs, files)

            
            


smart_htmlreport(dir_output)
