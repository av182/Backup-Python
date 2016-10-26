#!/usr/bin/python3

import os, sys
import shutil
import datetime
import filecmp
import time

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