# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime
import filecmp

if len(sys.argv) != 3:
    print('Not enough arguments!')
    print('Usage: Backup_full.py sourse_dir target_dir')
    #sys.exit()
    backup_from = r'D:\PY\tb'
    backup_to = r'D:\PY\backup'
else:
    backup_from = sys.argv[1]
    backup_to = sys.argv[2]

def source_count(pth):
    dirs_src = 0
    files_src = 0
    ptree = os.walk(backup_from)
    for dirpath, dirnames, filenames in ptree:
        dirs_src = dirs_src + len(dirnames)
        files_src = files_src + len(filenames)
    return dirs_src, files_src

print('Dirs in the source before backup: ',source_count(backup_from)[0])
print('Files in the source before backup: ',source_count(backup_from)[1])

files_to_be_copied = []
files_copied = []
files_identical = []
files_different = []
files_copy_error = []
now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_full')
dstfolder = os.path.join(backup_to, now_time)
os.mkdir(dstfolder)
ptree = os.walk(backup_from)
item_in_path_to_backup = len(backup_from.split('\\'))
ii=0
for dirpath, dirnames, filenames in ptree:
    ii=ii+1
    src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
    dstpath=dstfolder
    for folders in src_list_path:
        dstpath = os.path.join(dstpath, folders)   
        #dstpath = dstpath+'\\'+folders 
    
#Making directories
    for dirs in dirnames:
        dircheck = os.path.join(dstpath, dirs)
        if not os.path.exists(dircheck):
            os.makedirs(dircheck)
        else:
            if not os.path.isdir(dircheck):
                os.remove(dircheck)
                os.makedirs(dircheck)
                print("Not a folder detected!")

#Copying files
    for fl in filenames:
        fullsrcpath = os.path.join(dirpath, fl)
        fulldstpath = os.path.join(dstpath, fl)
        files_to_be_copied.append(fullsrcpath)
        try:
            shutil.copy2(fullsrcpath, fulldstpath)
            files_copied.append(fullsrcpath)
        except IOError as e:
            files_copy_error.append(fullsrcpath)
            #'file name is too long' exception handling
            if len(fulldstpath)>259:
                print ('Skipping file: ', fulldstpath,' Destination path is to long -> ', len(fulldstpath))
            else:
                print('Skipping', fullsrcpath, e.errno, e.strerror)
            continue
        try:
            compare_result = filecmp.cmp(fullsrcpath, fulldstpath, shallow=False)
            if compare_result:
                files_identical.append(fullsrcpath)
            else:
                files_different.append(fulldstpath)
        except IOError as e:
            print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!', e.errno, e.strerror)
   
print('Files ready to be copied - ', len(files_to_be_copied))
print('Files copied - ', len(files_copied))
print('Files not copied - ', len(files_copy_error))
print('Files identical - ', len(files_identical))
print('Files different - ', len(files_different))   
    