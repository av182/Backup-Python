# -*- coding: utf-8 -*-
import os, sys
import shutil
import datetime
import filecmp
import time

start = time.time()

if len(sys.argv) < 3:
    print('Not enough arguments!')
    print('Usage: Backup_full.py sourse_dir target_dir -n(optional)')
    #sys.exit()
    no_compare = False
    backup_from = r'D:\PY\tb'
    backup_to = r'D:\PY\backup'
elif len(sys.argv) == 3:
    backup_from = sys.argv[1]
    backup_to = sys.argv[2]
    no_compare = False
elif len(sys.argv) == 4:
    if sys.argv[3] == '-n':
        no_compare = True
    else:
        print("Bad argument. Need '-n' for non-comparsion backup")
        sys.exit()
    backup_from = sys.argv[1]
    backup_to = sys.argv[2]
else:
    print('Too many arguments!')
    print('Usage: Backup_full.py sourse_dir target_dir -n(optional)')
    sys.exit()

def source_count(pth):
    print("Gathering statistics...")
    dirs_src = 0
    files_src = 0
    total_size = 0
    ptree = os.walk(backup_from)
    for dirpath, dirnames, filenames in ptree:
        dirs_src = dirs_src + len(dirnames)
        files_src = files_src + len(filenames)
        for fl in filenames:
            fullsrcpath = os.path.join(dirpath, fl)
            total_size = total_size + os.path.getsize(fullsrcpath)
    return dirs_src, files_src, total_size

#Logging file copied files
log = open(r'D:\PY\lglglg.log', 'w')    
def write_log(log_str):
    try:
        log.write(log_str+ '\n')
    except:
        log.write('Encode error\n')
        
source_stat = source_count(backup_from)
print('   Dirs in the source before backup: ',source_stat[0])
print('   Files in the source before backup: ',source_stat[1])
print('   Total size before backup: ',source_stat[2],'bytes (', round(source_stat[2]/1024/1024, 2), ' Mb)')
print('-----------------------------------------------------')

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
print('Copying files...')
print('')
ii=0
for dirpath, dirnames, filenames in ptree:
    #ii=ii+1
    src_list_path = dirpath.split('\\')[item_in_path_to_backup:]
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

#Copying files
    for fl in filenames:
        fullsrcpath = os.path.join(dirpath, fl)
        fulldstpath = os.path.join(dstpath, fl)
        files_to_be_copied.append(fullsrcpath)
        #ii=ii+1
        #print(ii)
        write_log(fl)
        try:
            shutil.copy2(fullsrcpath, fulldstpath)
            files_copied.append(fullsrcpath)
        except IOError as e:
            files_copy_error.append(fullsrcpath)
            #'file name is too long' exception handling
            if len(fulldstpath)>259:
                print ('Skipping file: ', fulldstpath,' Destination path is too long -> ', len(fulldstpath))
            else:
                print('Skipping', fullsrcpath, e.errno, e.strerror)
            continue
        if not no_compare:
            try:
                compare_result = filecmp.cmp(fullsrcpath, fulldstpath, shallow=False)
                if compare_result:
                    files_identical.append(fullsrcpath)
                else:
                    files_different.append(fulldstpath)
                    print('Difference in file - ', fullsrcpath)
            except IOError as e:
                print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!', e.errno, e.strerror)
log.close()
print('')  
print('-----------------------------------------------------')
print('Files ready to be copied - ', len(files_to_be_copied))
print('Files copied - ', len(files_copied))
print('Skipped files - ', len(files_copy_error))
if not no_compare:
    print('Comparsion results:')
    print('   Files identical - ', len(files_identical))
    print('   Files different - ', len(files_different)) 
dst_stat = source_count(dstfolder)
print('   Total size after backup: ',dst_stat[2],'bytes (', round(dst_stat[2]/1024/1024, 2), ' Mb)')
print('Size difference before and after backup- ', source_stat[2]-dst_stat[2], 'bytes')
print('Backup time - ', round(time.time()-start, 2), 'sec (', round((time.time()-start)/60, 2),'min)')   
