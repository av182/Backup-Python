# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime
import filecmp

path_collection = []
backup_from = 'D:\\PY\\tb'
backup_to = 'D:\\PY\\backup'
files_identical = 0
files_different = 0

def find_prev_full_backup_folder():
    """finding out the previous full_backup folder in the backup directory"""
    prev_backup_tree = os.listdir(path=backup_to)
    full_backup_tree = []
    for dirs in prev_backup_tree:
        if dirs.find('_full') != -1:
            full_backup_tree.append(dirs) 
    #checking if there are any "_full"-backup directory found. Exit, if not
    if full_backup_tree != []:
        prev_full_backup = max(full_backup_tree)
    else:
        print('Directories with full backups not found. Exit...')
        sys.exit()
    print(full_backup_tree)
    return prev_full_backup

def compare(fs, fd):
    """Compares 2  files byte-by-byte for identical(filecmp lib)"""
    global files_identical
    global files_different
    try:
        compare_result = filecmp.cmp(fs, fd, shallow=False)
        if compare_result:
            print('Source and destination files are identical')
            files_identical = files_identical + 1
            print('Files IDEN - ', files_identical)
        else:
            print('Source and destination files are DIFFERENT')
            files_different = files_different + 1
    except IOError as e:
        print('Comparsion ',fs, ' and ', fd, ' failed!', e.errno, e.strerror)

#finding out previous full backup path
last_full_backup_folder = find_prev_full_backup_folder()
path_prev_full_backup = os.path.join(backup_to, last_full_backup_folder)
print("Path to previous full backup --> ",path_prev_full_backup)

#make backup destination folder
now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_differ')
dstfolder = os.path.join(backup_to, now_time)
os.mkdir(dstfolder)

#scaning source folder (script main operation)
item_in_path_to_backup = len(backup_from.split('\\'))
ptree = os.walk(backup_from)
ii=0
for dirpath, dirnames, filenames in ptree:
    ii=ii+1
    print(ii)
    print('Where we are now(dirpath) - ',dirpath)
    print('Directories in current point(dirnames) - ',dirnames)    
    src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
    full_current_point=path_prev_full_backup
    dstpath = dstfolder
    print('Folder in dirpath to be added to dstpath at this step(src_list_path) - ',src_list_path)
    for folders in src_list_path:
        full_current_point = os.path.join(full_current_point, folders)
        dstpath = os.path.join(dstpath, folders)
    print("Where we are gonna check for file presence(full_current_point) - ", full_current_point)
    print("Where we are gonna copy to (dstpath) - ", dstpath)
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
        fullprevpath = os.path.join(full_current_point, file)
        path_collection.append(fullsrcpath)
        if (not os.path.exists(fullprevpath)) or \
           (os.path.getsize(fullsrcpath) != os.path.getsize(fullprevpath)) or \
           (os.path.getmtime(fullsrcpath) != os.path.getmtime(fullprevpath)):
            try:
                shutil.copy2(fullsrcpath, fulldstpath)
                compare(fullsrcpath, fulldstpath)
                print('File copied and checked.')
            except IOError as e:
                print('skipping', fullsrcpath, e.errno, e.strerror)
                continue
        else:
            #if os.path.getsize(fullsrcpath) == os.path.getsize(fullprevpath):
            print('File exist in full backup. Skiping...')

print('Files copied - ', len(path_collection))
print('Files identical - ', files_identical)
print('Files different - ', files_different)   

