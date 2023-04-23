# Folder Synchronization Script
This is a Python script that synchronizes two directories by copying and updating files from the source directory to the target directory. It uses the MD5 hash algorithm to compare the content of files and decides whether to update or copy them. It also removes files and directories that exist in the target directory but not in the source directory.
 A log file is created at the specified path, and all log messages are written to this file. Additionally, the log messages are printed on the console using a StreamHandler().

## Usage
To use the script, run the following command:
```
python sync_folders.py --src /path/to/source/directory --dst /path/to/target/directory --interval 60 --log /path/to/log/file.log
```

For example:
```
python sync_folders.py C:\source_folder C:\replica_folder 30 C:\log_file.txt
```

This will synchronize the source folder `C:\source_folder` with the replica folder `C:\replica_folder` every 30 seconds, and log all file operations to `C:\log_file.txt`

