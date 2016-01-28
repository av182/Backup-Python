# Backup-Python
Backup scripts (full, differential, incremental). Also compares each file after backup for correctness.

Backup_full.py:

usage: "Backup_full.py backup_from_folder backup_to_folder" -- Backup and byte-by-byte compare each file .

"Backup_full.py backup_from_folder backup_to_folder -n" -- Backup without compare backuped files.
       
Example: Backup_full.py "D:\backup_from" "\\server\backup_to"  -- creates folder like that "28012016-170514_full" and backup all the source tree into it. After copy of each file - byte-by-byte compares it with original file in the source directory.  

Project is NOT DONE yet (under development)!

What is the purpose?
Making a script(or scripts) that will make full, 
then differential or incremental backup of a source folder on Windows nerwork share to target folder on Linux machine.
When each file is copied, it must be compared (some stats, byte-by-byte or hash) with its original source file for integrity. 
And some logs must be made, of course...

Backup_full.py - make full backup of the source folder.
backup_differential.py - make a differential backup based on previous full backup.
test.py - notning usefull, just small tests for me.

Linux_version - Linux version of the scripts. Will be inegrated in main scripts later.

If you find it usefull anyhow, it would be great!
