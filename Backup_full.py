# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime

path_collection = []
backup_type = 'incremental'
backup_from = 'D:\\PY\\tb'
backup_to = 'D:\\PY\\backup'
now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_full')
dstfolder = os.path.join(backup_to, now_time)
os.mkdir(dstfolder)
print(now_time)
ptree = os.walk(backup_from)
item_in_path_to_backup = len(backup_from.split('\\'))
ii=0
for dirpath, dirnames, filenames in ptree:
    ii=ii+1
    print(ii)
    print('Where we are now(dirpath) - ',dirpath)
    print('Directories in current point(dirnames) - ',dirnames)
    print('Files in current point(filenames) - ',filenames)    
    src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
    print('Folder in dirpath to be added to dstpath at this step - ',src_list_path)
    print('----------------------------------------------')
    dstpath=dstfolder
    #print("DIRPATH (где находимся)- "+dirpath)
    for folders in src_list_path:
        dstpath = dstpath+'\\'+folders 
    #print("Куда будем копировать - "+dstpath)
  
#Делаем директории
    for dirs in dirnames:
        dircheck = os.path.join(dstpath, dirs)
        if not os.path.exists(dircheck):
            os.makedirs(dircheck)
        else:
            if not os.path.isdir(dircheck):
                os.remove(dircheck)
                os.makedirs(dircheck)
                print("Not a folder detected!")
#Копируем файлы
    for file in filenames:
        fullsrcpath = os.path.join(dirpath, file)
        fulldstpath = os.path.join(dstpath, file)
        path_collection.append(fullsrcpath)
        try:
            shutil.copy2(fullsrcpath, fulldstpath)
        except os.error:
            print('skipping', fullsrcpath, sys.exc_info()[0])

    
    
    
