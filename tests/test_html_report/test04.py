import os

dir_output = './dirout'
abs_dir_output = os.path.abspath(dir_output)
print(abs_dir_output)

for rootpath, dirs, files in os.walk(dir_output):
    if os.path.isabs(dir_output):
        walk_deep = rootpath[len(abs_dir_output):].count(os.sep)
    else:
        walk_deep = rootpath.count(os.sep) - 1
    #if walk_deep > 5:break    
    print(rootpath, '\t', walk_deep)


    
