#!/usr/bin/python3

import os, sys
import shutil
import datetime
import filecmp
import time

start = time.time()

log = open(r'D:\PY\testtest.log', 'w')

def source_count(pth):
    print("getting statistics...")
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
    return dirs_src, files_src, total_size
'''
dst_stat = source_count(r'D:\py\tb')
print('   Total size after backup: ',dst_stat[2],'bytes (', round(dst_stat[2]/1024/1024, 2), ' Mb)')
print('Backup time - ', round(time.time()-start, 2), 'sec (', round((time.time()-start)/60, 2),'min)')
'''
'''
def list_dir(dr):
	print(dr,file=log)
	dir_tree = os.listdir(dr)
	print(len(dir_tree))
	for i in dir_tree:
		#try:

		drb = dr.encode('utf-16')
		dr2 = r'D:\py\tb2'
		drb2 = dr2.encode('utf-16')
		#print(drb2)
		print(drb,file=log)
		print(drb[2:],file=log)
		flb = i.encode('utf-16')
		print(flb,file=log)
		print('')
		print(os.path.join(drb,flb[2:]), file=log)
		shutil.copyfile(os.path.join(drb,flb[2:], os.path.join(drb2,flb[2:]))
		#print('')
		#ddd = os.path.join(dr.encode('utf-16'))
		#print(ddd+i.encode('utf-16'))
		#print('Second encoding  ',os.path.join(dr.encode('utf-16'),i),file=log)
		#shutil.copyfile(dr.join(i), r'D:\py\tb1'.join(i))
'''	
'''	
		#print(os.fsencode(i))
		#except:
			#print(os.fsencode(i))
			#continue
	print(dir_tree[1])
	fullpath = os.path.join(dr,dir_tree[1])
	print(fullpath)
	shutil.copyfile(os.path.join(dr,dir_tree[12]), r'D:\PY\tb\f1\a.txt'.encode('utf-8'))'''
#list_dir(r'D:\py\tb1')
#print('D:\py\tb'.encode('utf-16'))


dr = r'D:\py\tb1'
drb = dr.encode('utf-16')
dr2 = r'D:\py\tb2'
drb2 = dr2.encode('utf-16')
fl = r'ДОВЕРЕННОСТЬ «G ÄÄÄ.docx'
fse = os.fsencode(fl)
flb = fl.encode('utf-16')
#shutil.copy2(os.path.join(dr,fl), os.path.join(dr2,fl))
