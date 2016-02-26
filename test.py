import os, sys
import shutil
import datetime
import filecmp
'''
backup_from = r'D:\PY\tb'
#backup_from = 'D:\py'
item_in_path_to_backup = len(backup_from.split(os.sep))
for itm in backup_from.split(os.sep):
	print('- ',itm)
print('item_in_path_to_backup: ',item_in_path_to_backup)
#dirpath = r'd:\py\1\2\3'
dirpath = r'D:\PY\backup\1\2\3'
src_list_path = dirpath.split(os.sep)[item_in_path_to_backup:]
print(src_list_path)
'''
'''
src = r'D:\py\tmp\test.txt'
dst = r'D:\py\tmp\2\test.txt'
#shutil.copy2(src,dst)
compare_result = filecmp.cmp(src, dst)
print(compare_result)
'''
fs_enc = sys.getfilesystemencoding() 
print(fs_enc)
path_collection = os.listdir(r'D:\PY\tb')
rootdir = r'D:\PY\tb'
spisok = os.listdir(rootdir.encode(fs_enc))
for item in spisok:
	try:
		print(item.decode(fs_enc))
	except:
		print('ERROR -> ',item)
'''for pth in path_collection:
    try:
        print(repr(pth))
    except UnicodeEncodeError:
        print('Error:')
        print(u(pth))'''
