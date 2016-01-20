# -*- coding: utf-8 -*-
import os
import shutil
import datetime

path_collection = []
backup_type = 'incremental'
raw_sourcefolder = r'D:\distr\zwc\ecl'
raw_dstfolder = r'D:\PY\backup'
now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_full')
dstfolder = os.path.join(raw_dstfolder, now_time)
os.mkdir(dstfolder)
print(now_time)
ptree = os.walk(raw_sourcefolder)
item_in_path_to_backup = len(raw_sourcefolder.split('\\'))
ii=0
for dirpath, dirnames, filenames in ptree:
    ii=ii+1
    print(ii)
    print(dirnames)    
    src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
    dstpath=dstfolder
    print("DIRPATH (где находимся)- "+dirpath)
    for folders in src_list_path:
        dstpath = dstpath+'\\'+folders 
    print("Куда будем копировать - "+dstpath)
  
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
        shutil.copy2(fullsrcpath, fulldstpath)
    
    
    
