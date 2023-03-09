# sync_folders

## Description
This is a Python script that synchronizes two directories at a specified interval using MD5 checksums to compare files.


## Usage
To use this program, run it from the command line with the following arguments:

* source: the path to the source folder to synchronize.
* replica: the path to the replica folder to synchronize.
* interval: the synchronization interval in seconds.
* log_file: the path to the log file to create.

For example:
```
python sync_folders.py C:\source_folder C:\replica_folder 60 C:\log_file.txt
```

This will synchronize the source folder `C:\source_folder` with the replica folder `C:\replica_folder` every 60 seconds, and log all file operations to `C:\log_file.txt`

### Overview

1. Create a Pipenv
```
pipenv install
```
2. Activate the pipenv environment by running the following command:
```
 pipenv shell
```
3. Run the python script in Pipenv
```
pipenv run python sync_folders.py --src [source folder] --dst ./replica --interval [time in seconds] --log [log file e.G. log.txt]
```
4. To break, use the keyboard shortcut `Ctrl + C`
5. Once you're done running the script, deactivate the pipenv environment by running the following command:
```
exit
```

pipenv run python sync_folders.py --src source --dst replica --interval 60 --log log.txt
