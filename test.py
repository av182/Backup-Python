#!/usr/bin/python3

import os, sys
import shutil
import datetime
import filecmp
import time


backup_from = r'\\10.100.48.30\c$\Агентирование'
#backup_from = r'D\py\tb'
dirpath = r'\\10.100.48.30\c$\Агентирование\12312\222'
item_in_path_to_backup = len(backup_from.split(os.sep))
src_list_path = dirpath.split(os.sep)[item_in_path_to_backup:]
print(item_in_path_to_backup)
print(src_list_path)
for i in backup_from.split(os.sep):
    print(i)
