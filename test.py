import os, sys
import shutil
import datetime
import filecmp

backup_from = '/mnt/tb'
#backup_from = 'D:\py'
item_in_path_to_backup = len(backup_from.split('/'))
for itm in backup_from.split('/'):
	print('- ',itm)
print('item_in_path_to_backup: ',item_in_path_to_backup)
#dirpath = r'd:\py\1\2\3'
dirpath = '/mnt/tb/1/2/3'
src_list_path = dirpath.split('/')[item_in_path_to_backup:]
print(src_list_path)
'''
src = r'D:\py\tmp\test.txt'
dst = r'D:\py\tmp\2\test.txt'
#shutil.copy2(src,dst)
compare_result = filecmp.cmp(src, dst)
print(compare_result)
'''