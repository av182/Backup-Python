# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime
import filecmp

path_collection = []
backup_type = 'incremental'
backup_from = r'D:\PY\tb'
backup_to = r'D:\PY\backup'
now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_full')
dstfolder = os.path.join(backup_to, now_time)
os.mkdir(dstfolder)
print(now_time)
ptree = os.walk(backup_from)
item_in_path_to_backup = len(backup_from.split('\\'))
ii=0
files_identical = 0
files_different = 0
for dirpath, dirnames, filenames in ptree:
    ii=ii+1
    print(ii)
    print('Where we are now(dirpath) - ',dirpath)
    print('Directories in current point(dirnames) - ',dirnames)
    print('Files in current point(filenames) - ',filenames)    
    src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
    print('Folder in dirpath to be added to dstpath at this step - ',src_list_path)
    dstpath=dstfolder
    for folders in src_list_path:
        dstpath = os.path.join(dstpath, folders)   
        #dstpath = dstpath+'\\'+folders 
    print("Where we are gonna copy - "+dstpath)
    print('----------------------------------------------')
  
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
    for file in filenames:
        fullsrcpath = os.path.join(dirpath, file)
        fulldstpath = os.path.join(dstpath, file)
        path_collection.append(fullsrcpath)
        try:
            shutil.copy2(fullsrcpath, fulldstpath)
        except IOError as e:
            print('skipping', fullsrcpath, e.errno, e.strerror)
            continue
        try:
            compare_result = filecmp.cmp(fullsrcpath, fulldstpath, shallow=False)
            if compare_result:
                #print('Source and destination files are identical')
                files_identical = files_identical+1
            else:
                #print('Source and destination files are DIFFERENT')
                files_different = files_different+1
        except os.error:
            print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!', e.errno, e.strerror)
   
print(path_collection)
print('Files copied - ', len(path_collection))
print('Files identical - ', files_identical)
print('Files different - ', files_different)   
    
