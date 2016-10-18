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
    dirs_src = 1
    files_src = 2
    total_size = 3   
    return dirs_src, files_src, total_size
ddd = source_count('dfgdf')
print(ddd)