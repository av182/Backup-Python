import os, sys
import shutil
import datetime
import filecmp

path_to_clean = r'D:\PY\backup\26012016-155103_differ'

def del_empty_folders(kat, P = True):
	if os.path.isdir(kat):
		if len(os.listdir(kat)) > 0:
			for x in os.listdir(kat):
				if os.path.isdir(os.path.join(kat,x)):
					if len(os.listdir(os.path.join(kat,x))) == 0:
						try:
							os.rmdir(os.path.join(kat,x))
						except OSError as e:
							print('Failed to delete: ',os.path.join(kat,x),'.  Error - ', e.errno, e.strerror)
					else: del_empty_folders(os.path.join(kat,x))
			if P: del_empty_folders(kat, False)
		#else: os.rmdir(kat)

#del_empty_folders(path_to_clean)

print(sys.getfilesystemencoding())

"""
fullsrcpath = 'D:/PY/win.txt'
fulldstpath = 'D:/PY/backup/25012016-111908_full/Folder1/Папка3/win.txt'

try:
	compare_result = filecmp.cmp(fullsrcpath, fulldstpath, shallow=False)
	if compare_result:
		print('Source and destination files are identical')
		
	else:
		print('Source and destination files are DIFFERENT')
		
except os.error:
   	print('Comparsion ',fullsrcpath, ' and ', fulldstpath, ' failed!', sys.exc_info()[0])

print(os.path.getsize('D:/PY/win.txt'))
print(os.path.getsize('D:/PY/backup/25012016-111908_full/Folder1/Папка3/win.txt'))
print(os.path.getmtime('D:/PY/win.txt'))
print(os.path.getmtime('D:/PY/backup/25012016-111908_full/Folder1/Папка3/win.txt'))
"""