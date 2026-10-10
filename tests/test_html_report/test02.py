import os

dir_output = '../dirout'

images_file_path_list = [
    '../dirout/aa/SI11.svg', 
    '../dirout/aa/DOX.svg', 
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
    '../dirout/bb/ll/kk/SOL#dib7(no5)_FA#.svg', 
    '../dirout/bb/ll/kk/LA.svg',
    '../dirout/bb/png/ZZZ.png', 
    '../dirout/bb/png/XXX.png', 
    '../dirout/bb/png/YYY.png', 
    '../dirout/bb/ii/png/RE#m.png', 
    '../dirout/bb/ii/ww/png/SOL7.png', 
    '../dirout/bb/ii/qq/png/SOL.png', 
    '../dirout/bb/hh/png/DO9.png', 
    '../dirout/bb/ll/png/RE#dib7.png', 
    '../dirout/bb/ll/kk/png/LA.png', 
    '../dirout/bb/ll/kk/png/SOL#dib7(no5)_FA#.png', 
    '../dirout/bb/gg/png/DO7+.png', 
    '../dirout/bb/ff/png/DO7.png', 
    '../dirout/aa/png/ZAP.png', 
    '../dirout/aa/png/SI11.png', 
    '../dirout/aa/png/DOW.png', 
    '../dirout/aa/png/DOY.png', 
    '../dirout/aa/png/DOX.png', 
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

for rootpath, dirs, files in os.walk(dir_output): print(rootpath, dirs, files)


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
        
        filtered_files = []
        filtered_dirs = []
        for rootpath, dirs, files in os.walk(dir_output):

            # filtering certain file types
            for fname in files:
                f_path = os.path.join(rootpath, fname)
                if f_path in images_file_path_list:
                    filtered_files.append(f_path)
                    
            # filtering dirs
            for mydir in dirs:
                c_path = os.path.join(rootpath, mydir)
                if c_path in images_grouped_dir_list:
                    filtered_dirs.append(rootpath)

        filtered_sorted_files = sorted(filtered_files)
        filtered_sorted_grouped_dirs = sorted(list(set(filtered_dirs)))
        
        n_files = len(filtered_sorted_files)
        n_dirs = len(filtered_sorted_grouped_dirs)
        
        print(filtered_sorted_files)
        print(filtered_sorted_grouped_dirs)
        print(n_files)
        print(n_dirs)
            
            


smart_htmlreport(dir_output, 4, '200.0px')
