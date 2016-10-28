#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime
import filecmp
import time

'''
usage: "Backup_full.py backup_from_folder backup_to_folder".  Backup and compare each file by attributes (getmtime and size).
       "Backup_full.py backup_from_folder backup_to_folder -n". Backup without compare backuped files.
'''

start = time.time()
backup_from = ''
backup_to = ''
files_copied = []
files_identical = []
files_different = []
files_copy_error = []
files_renamed = []
files_in_source = 0
i = 0
no_compare = False

def usage():
    print('\nUsage:')
    print('Backup_full.py backup_from_folder backup_to_folder. Backup and compare each file byte-by-byte.')
    print('Backup_full.py backup_from_folder backup_to_folder -n. Backup without compare backuped files.')

#checking and initializing source and destination folder variable
def check_make_path(src, dst):
    if src.lower() == dst.lower():
        print('Source and Destination are identical. Exit...')
        usage()
        sys.exit()
    elif not os.path.exists(src):
        print('Source folder is not exist. Exit...')
        usage()
        sys.exit()
    elif not os.path.exists(dst):
        print('Destination folder is not exist. Exit...')
        usage()
        sys.exit()
    elif not os.path.isdir(src):
        print('Source path is not a folder. Exit...')
        usage()
        sys.exit()
    elif not os.path.isdir(dst):
        print('Destination path is not a folder. Exit...')
        usage()
        sys.exit()
    else:
        global backup_from
        global backup_to
        backup_from = src
        backup_to = dst

#checking arguments
if len(sys.argv) < 3:
    print('Not enough arguments!')
    usage()
    sys.exit()
    #backup_from = r'D:\PY\tb'
    #backup_to = r'D:\PY\tb1'
elif len(sys.argv) == 3:
    check_make_path(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    if sys.argv[3] == '-n':
        no_compare = True
    else:
        print('Bad argument!')
        usage()
        sys.exit()
    check_make_path(sys.argv[1], sys.argv[2])
else:
    print('Too many arguments!')
    usage()
    sys.exit()

#print number of dirs, files and total size of files in the given directory
def files_count(stat_title, pth):
    print('\n',stat_title)
    dirs_src = 0
    files_src = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(pth):
        dirs_src = dirs_src + len(dirnames)
        files_src = files_src + len(filenames)
        for fl in filenames:
            fullsrcpath = os.path.join(dirpath, fl)
            try:
                total_size = total_size + os.path.getsize(fullsrcpath)
                #total_size = total_size + os.lstat(fullsrcpath).st_size
            except IOError as e:
                if os.path.islink(fullsrcpath):
                    print('Broken symlink. Cannot check size: '+ fullsrcpath)
                else:
                    print('Warning. Cannot check file size: '+ fullsrcpath, e.errno, e.strerror)
                continue
    print('   Directories: ', dirs_src)
    print('   Files: ', files_src)
    print('   Total size: ',total_size,'bytes (', round(total_size/1024/1024, 2), ' Mb)')
    print('-----------------------------------------------------')
    #this will be needed in progress bar
    global files_in_source
    if (files_in_source==0):
        #file_count function will be called twice (before and after). We need before (source) files count
        #so we need to initialize file_in_source once.
        files_in_source=files_src

def final_stat():  
    print('\n-----------------------------------------------------')
    print('Files copied - ', len(files_copied))
    print('Skipped files - ', len(files_copy_error))
    print('Files renamed - ', len(files_renamed))
    if not no_compare:
        print('Comparsion results:')
        print('   Files identical - ', len(files_identical))
        print('   Files different - ', len(files_different)) 
        if len(files_different) != 0:
            for i in files_different:
                try:
                    print('Source file:')
                    print(i[0],' -> ',i[1],' -> ',i[2])
                    print('Destination file:')
                    print(i[3],' -> ',i[4],' -> ',i[5])
                except:
                    print('File name decode error. Cannot print to stdout')
    print('Backup time - ', round(time.time()-start, 2), 'sec (', round((time.time()-start)/60, 2),'min)')

#Logging copied files
#log = open(r'D:\PY\lglglg.log', 'w')    
def write_log(log_str):
    try:
        log.write(log_str+ '\n')
    except:
        log.write('Encode error\n')

def file_exist_warning(dst_check):
    if os.path.isfile(dst_check):
        print('Warning! File '+dst_check+' already exist in destination folder')

#checking if destination file path or name is too long and therefore destination file needs to be renamed before backup
def name_length_too_long(fullpath):
    if sys.platform.startswith('win32'):
        if len(fullpath)>259:
            return True
    elif sys.platform.startswith('linux'):
        if len(os.path.basename(fullpath).encode())>255:
            return True
    else:
        print('OS is not linux or win32. Exiting script...')
        sys.exit()
    return False

#rename file with too long name before backup 
def rename_file(file_to_rename):
    if sys.platform.startswith('win32'):
        return file_to_rename[:10]+'_'+file_to_rename[-10:]
    elif sys.platform.startswith('linux'):
        return file_to_rename[:70]+'_'+file_to_rename[-30:]


#progrees bar implementation
def progress_bar(ii):
    global files_in_source
    one_percent = round(files_in_source/100)
    if files_in_source >= 100:
    #if source files >= 100, percentage goes to stdout
        if ii%one_percent == 0 and ii//one_percent<=100:
            print(ii//one_percent, end=' ', flush=True)
    else:
        #if source files < 100, number of the copying file goes to stdout instead (because of 'by zero division')
        print('Files copied: ', ii, flush=True)

#time formatting
def time_format(tm):
    return datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S')

#Statistics BEFORE backup
files_count("Getting statistics in source BEFORE backup...", backup_from)

now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_full')
dstfolder = os.path.join(backup_to, now_time)
os.mkdir(dstfolder)
ptree = os.walk(backup_from)
item_in_path_to_backup = len(backup_from.split(os.sep))
print('Backup from: ',backup_from)
#print('Item in path to backup: ', item_in_path_to_backup)
print('Copying files... See percents below... Progress is based on count(not size) of the source files and may sometimes freeze for a while.')
print('')
for dirpath, dirnames, filenames in ptree:
    #i=i+1
    src_list_path = dirpath.split(os.sep)[item_in_path_to_backup:]
    dstpath=dstfolder
    for folders in src_list_path:
        dstpath = os.path.join(dstpath, folders)   
    
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
            else:
                print('Target dir already exist! Recreating...')

#Copying files
    try:
        for fl in filenames:
            fullsrcpath = os.path.join(dirpath, fl)
            fulldstpath = os.path.join(dstpath, fl)

            i=i+1
            progress_bar(i)

            #checking if source dir and file are exist at the moment of backup 
            if not os.path.isdir(dirpath):
                print('Directory is missing at the moment of backup. Skipping directory. ',dirpath)
                break
            if not os.path.isfile(fullsrcpath):
                print('File is missing at the moment of backup. Skipping. ',fullsrcpath)
                continue

            #file_copying is needed when interrupt occurs (last file that was being copied before interrupt)
            file_copying = fullsrcpath
            
            #saving mtime and size of the source file
            mtime_source = os.path.getmtime(fullsrcpath)
            size_source = os.path.getsize(fullsrcpath)
            '''
            #test
            if fl=='123.txt':
                    fl_test = open(fullsrcpath,'a')
                    print('2',file=fl_test)
                    fl_test.close()'''


            #write_log(fl)

            try:
                file_exist_warning(fulldstpath)
                shutil.copy2(fullsrcpath, fulldstpath, follow_symlinks=False)
                files_copied.append(fullsrcpath)
                

            except IOError as e:
                if name_length_too_long(fulldstpath):
                    try:
                        print ('\nTrying to rename: ', fullsrcpath,' File name is too long -> ', len(fl.encode()), ' bytes. ', len(fulldstpath), ' characters.')
                    except:
                        print('\nTrying to rename file but cannot print its name (decode error)')
                    new_name = rename_file(fl)
                    print('New name - ',new_name)
                    fulldstpath = os.path.join(dstpath, new_name)
                    file_exist_warning(fulldstpath)
                    try:
                        shutil.copy2(fullsrcpath, fulldstpath)
                        files_copied.append(fullsrcpath)
                        files_renamed.append(fullsrcpath)
                    except:
                        print ('\nErrors while copying renamed file. Skipping file: ', fulldstpath)
                        files_copy_error.append(fullsrcpath)
                        continue
                else:
                    print('\nSkipping', fullsrcpath, e.errno, e.strerror)
                    files_copy_error.append(fullsrcpath)
                    continue

            #saving mtime and size of the destination file       
            mtime_dest = os.path.getmtime(fulldstpath)
            size_dest = os.path.getsize(fulldstpath)

            #comparsion implementation
            if not no_compare:
                try:
                    #print('Comparing ',fullsrcpath, ' -> ', fulldstpath)
                    if (mtime_source==mtime_dest and size_source==size_dest):
                        files_identical.append(fulldstpath)
                    else:
                        print('Difference in file - ', fulldstpath)

                        files_different.append([fullsrcpath, time_format(mtime_source), size_source, fulldstpath, time_format(mtime_dest), size_dest])
                except IOError as e:
                    print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!', e.errno, e.strerror)
    except KeyboardInterrupt:
        print('\nOK. exit...')
        files_count("\nStatistics IN DESTINATION after INTERRUPT",dstfolder)
        final_stat()
        print('File copying before interrupt - ', file_copying )
        sys.exit()
print('\n-----------------------------------------------------')
files_count("\nStatistics IN DESTINATION after backup",dstfolder)
final_stat()
#log.close()