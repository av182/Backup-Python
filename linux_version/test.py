#!/usr/bin/Python-3.5.1/python
# -*- coding: utf-8 -*-

import os, sys
import shutil
import datetime
import filecmp

log = open(r'/home/user/py.log', 'w')
ttt = '/mnt/winf/tb'
log.write('TEST\n')
lst = os.listdir(ttt.encode())
print(lst)
def write_log(log_str):
	for items in log_str:
		log.write(items+'\n')
write_log(lst)	
log.close()
'''
fullsrcpath = '/mnt/winf/doc2.txt'
fulldstpath = '/home/user/bck/dc2.txt'

try:
	compare_result = filecmp.cmp(fullsrcpath, fulldstpath, shallow=False)
	if compare_result:
		print('Source and destination files are identical')
		
	else:
		print('Source and destination files are DIFFERENT')
		
except os.error:
   	print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!')

print(os.path.getsize(fullsrcpath))
print(os.path.getsize(fulldstpath))
print('lalala')
'''