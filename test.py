import os, sys
import shutil
import datetime
import filecmp


def func():
    print("func() in one.py")

print("top-level in one.py")

if __name__ == "__main__":
    print("one.py is being run directly")
else:
    print("one.py is being imported into another module")

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