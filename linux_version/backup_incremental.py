# -*- coding: utf-8 -*-
import os
import shutil
import datetime

path_collection = []
backup_type = 'incremental'
raw_sourcefolder = r'D:\distr\zwc\ecl'
raw_dstfolder = r'D:\PY\backup'

#finding out the previous full_backup folder in the backup directory
def find_prev_full_backup_folder():
    prev_backup_tree = os.listdir(path=raw_dstfolder)
    full_backup_tree = []
    for dirs in prev_backup_tree:
        if dirs.find('-full') != -1:
            full_backup_tree.append(dirs) 
    prev_full_backup = max(full_backup_tree)
    print(full_backup_tree)
    return prev_full_backup

#finding out previous full backup path
last_full_backup_folder = find_prev_full_backup_folder()
path_prev_full_backup = os.path.join(raw_dstfolder, last_full_backup_folder)
print("Path to previous full backup --> ",path_prev_full_backup)

#make backup destination folder
now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S-increm')
dstfolder = os.path.join(raw_dstfolder, now_time)
#os.mkdir(dstfolder)

#scaning source folder (script main operation)
item_in_path_to_backup = len(raw_sourcefolder.split('\\'))
ptree = os.walk(raw_sourcefolder)
ii=0
for dirpath, dirnames, filenames in ptree:
    ii=ii+1
    if ii==3:
        print(ii)
        #print(dirnames)    
        src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
        prev_full_current=path_prev_full_backup
        current_backup = dstfolder
        print("DIRPATH (где находимся)- "+dirpath)
        print("Где полный бэкап текущий 1- "+prev_full_current)
        print(src_list_path)
        for folders in src_list_path:
            prev_full_current = prev_full_current +'\\'+folders
            current_backup = current_backup +'\\'+folders
        print("Где полный бэкап текущий - "+prev_full_current)
        print("Текущий путь текущего бэкапа - "+current_backup)
    
    
    
    
"""  
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
        time_src = os.path.getmtime(fullsrcpath)
        #time_dst = os.path.getmtime(fulldstpath)
        #print(os.path.getmtime(fullsrcpath))
        path_collection.append(fullsrcpath)
        shutil.copy2(fullsrcpath, fulldstpath)"""
    
    
    
