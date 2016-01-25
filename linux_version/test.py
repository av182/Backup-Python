#!/usr/bin/Python-3.5.1/python
# -*- coding: utf-8 -*-

import os, sys
import shutil
import datetime
import filecmp

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