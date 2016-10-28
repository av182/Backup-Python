# Backup-Python
Cross-platform backup scripts. After copying each file - compares it with source for correctness.

Backup_full.py:

usage: "Backup_full.py backup_from_folder backup_to_folder".  Backup and compare each file by attributes (getmtime and size).
       "Backup_full.py backup_from_folder backup_to_folder -n". Backup without compare backuped files.
       
Example: Backup_full.py "D:\backup_from" "\\server\backup_to"  -- creates folder like that "28012016-170514_full" and backup all the source tree into it. After copy of each file -  compares it with original file in the source directory.  

Project is NOT DONE yet (under development)!

Backup_full.py - make full backup of the source folder.
backup_differential.py - make a differential backup based on previous full backup (Under development).
test.py - notning usefull, just small tests for me.

If you find it usefull anyhow, it would be great!
