#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime
import filecmp
import time

'''
usage: "Backup_full.py backup_from_folder backup_to_folder".  Backup and compare each file byte-by-byte.
       "Backup_full.py backup_from_folder backup_to_folder -a". Backup and compare only attributes of each file .
       "Backup_full.py backup_from_folder backup_to_folder -n". Backup without compare backuped files.
'''

start = time.time()
backup_from = ''
backup_to = ''
files_to_be_copied = []
files_copied = []
files_identical = []
files_different = []
files_copy_error = []
files_renamed = []
i = 0
ii = 0
no_compare = False
compare_only_attr = False

def usage():
    print('')
    print('Usage:')
    print('Backup_full.py backup_from_folder backup_to_folder. Backup and compare each file byte-by-byte.')
    print('Backup_full.py backup_from_folder backup_to_folder -a. Backup and compare only attributes of each file.')
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
    #sys.exit()
    no_compare = False
    backup_from = r'D:\PY\tb'
    backup_to = r'D:\PY\tb1'
elif len(sys.argv) == 3:
    check_make_path(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 4:
    if sys.argv[3] == '-n':
        no_compare = True
    elif sys.argv[3] == '-a':
        compare_only_attr = True
    else:
        print("Bad argument. Need '-n' for non-comparsion backup or '-a' for only files attributes comparsion")
        sys.exit()
    check_make_path(sys.argv[1], sys.argv[2])
else:
    print('Too many arguments!')
    usage()
    sys.exit()

def files_count(stat_title, pth):
    print(stat_title)
    dirs_src = 0
    files_src = 0
    total_size = 0
    ptree = os.walk(pth)
    for dirpath, dirnames, filenames in ptree:
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
    #return dirs_src, files_src, total_size

def final_stat():
    print('')  
    print('-----------------------------------------------------')
    print('Files ready to be copied - ', len(files_to_be_copied))
    print('Files copied - ', len(files_copied))
    print('Skipped files - ', len(files_copy_error))
    print('Files renamed and copied - ', len(files_renamed))
    if not no_compare:
        print('Comparsion results:')
        print('   Files identical - ', len(files_identical))
        print('   Files different - ', len(files_different)) 
    dst_stat = files_count(dstfolder)
    print('   Total size after backup: ',dst_stat[2],'bytes (', round(dst_stat[2]/1024/1024, 2), ' Mb)')
    print('Size difference before and after backup- ', source_stat[2]-dst_stat[2], 'bytes')
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

#Statistics BEFORE backup
files_count("Statistics BEFORE backup", backup_from)


now_time = datetime.datetime.now().strftime('%d%m%Y-%H%M%S_full')
dstfolder = os.path.join(backup_to, now_time)
os.mkdir(dstfolder)
ptree = os.walk(backup_from)
item_in_path_to_backup = len(backup_from.split(os.sep))
print('Backup from: ',backup_from)
print('Item in path to backup: ', item_in_path_to_backup)
print('Copying files... See percents below... Progress is based on count(not size) of files and may sometimes freeze for a while.')
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
            files_to_be_copied.append(fullsrcpath)
            i=i+1
            #write_log(fl)
            try:
                file_exist_warning(fulldstpath)
                shutil.copy2(fullsrcpath, fulldstpath, follow_symlinks=False)
                #rsync = 'rsync -a '+fullsrcpath+' '+fulldstpath
                #os.popen(rsync)
                files_copied.append(fullsrcpath)
                '''if fl=='123.txt':
                    fl_test = open(fullsrcpath,'a')
                    print('2',file=fl_test)
                    fl_test.close()'''
                #progress bar
                '''if source_stat[1] >= 100:
                    #if source files >= 100, percentage goes to stdout
                    if i%(source_stat[1]//100) == 0:
                        ii = ii + 1
                        print(ii, end=' ', flush=True)
                else:
                    #if source files < 100, file copied goes to stdout instead (because of 'by zero division')
                    ii = ii + 1
                    print('Files copied: ', ii, flush=True)'''

            except IOError as e:
                #'file name is too long' exception handling
                if sys.platform.startswith('linux'):
                    if len(fl.encode())>255:
                        try:
                            print ('\nTrying to rename: ', fulldstpath,' File name is too long -> ', len(fl.encode()), ' bytes. ', len(fl), ' characters.')
                            fulldstpath = os.path.join(dstpath, fl[:70]+'_'+fl[-30:])
                            file_exist_warning(fulldstpath)
                            shutil.copy2(fullsrcpath, fulldstpath)
                            print('New name: ', fl[:70]+'_'+fl[-30:])
                            files_renamed.append(fullsrcpath) 
                        except:
                            print ('\nSkipping file: ', fulldstpath,' File name is too long -> ', len(fl.encode()), ' bytes. ', len(fl), ' characters.')
                            files_copy_error.append(fullsrcpath)
                            continue
                    else:
                        print('\nSkipping', fullsrcpath, e.errno, e.strerror)
                        files_copy_error.append(fullsrcpath)
                        continue
                elif sys.platform.startswith('win32'):
                    if len(fulldstpath)>259:
                        try:
                            print ('\nTrying to rename: ', fulldstpath,' Destination path is too long -> ', len(fulldstpath))
                            fulldstpath = os.path.join(dstpath, fl[:10]+'_'+fl[-10:])
                            file_exist_warning(fulldstpath)
                            shutil.copy2(fullsrcpath, fulldstpath)
                            print('New name: ', fl[:10]+'_'+fl[-10:])
                            files_renamed.append(fullsrcpath)
                        except:
                            print ('\nSkipping file: ', fulldstpath,' Destination path is too long -> ', len(fulldstpath))
                            files_copy_error.append(fullsrcpath)
                            continue
                    else:
                        print('\nSkipping', fullsrcpath, e.errno, e.strerror)
                        files_copy_error.append(fullsrcpath)
                        continue
                else:
                    print('OS is not linux or win32. Exiting...')
                    sys.exit()

            #comparsion realization
            if not no_compare:
                try:
                    #print('Comparing ',fullsrcpath, ' -> ', fulldstpath)
                    compare_result = filecmp.cmp(fullsrcpath, fulldstpath, shallow=compare_only_attr)
                    if compare_result:
                        files_identical.append(fullsrcpath)

                    else:
                        files_different.append(fulldstpath)
                        print('Difference in file - ', fullsrcpath)
                except IOError as e:
                    print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!', e.errno, e.strerror)
    except KeyboardInterrupt:
        print('\nOK. exit...')
        files_count("Statistics IN DESTINATION after INTERRUPT",dstfolder)
        #final_stat()
        print('File copying before interrupt - ', files_to_be_copied[len(files_to_be_copied)-1] )
        sys.exit()

files_count("Statistics IN DESTINATION after backup",dstfolder)
#final_stat()
#log.close()
   
