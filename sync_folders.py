import os, logging, time, argparse
from hashlib import md5

# A function that uses argparse to parse command line arguments.
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, required=True,
                        help='Source directory to be synchronized')
    parser.add_argument('--dst', type=str, required=True,
                        help='Target directory to synchronize with')
    parser.add_argument('--interval', type=int, required=True,
                        help='Synchronization interval in seconds')
    parser.add_argument('--log', type=str, required=True,
                    help='Log file path')
    args = parser.parse_args()

    # Check if the source and target directories exist, and create them if they don't.
    for folder_name in [args.src, args.dst]:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f'Folder "{folder_name}" created successfully')
        else:
            continue
    return args

# A function that compares the MD5 hash of two files and returns True if they are the same.
def compare_files(src_file_path, dst_file_path):
    with open(src_file_path, 'rb') as src_f, open(dst_file_path, 'rb') as dst_f:
        return md5(src_f.read()).hexdigest() == md5(dst_f.read()).hexdigest()

# A function that synchronizes files between two directories.
def sync(src_dir, dst_dir):
    log = logging.getLogger('sync')

    # Iterate over the files in the source directory.
    for file_name in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, file_name)
        dst_file_path = os.path.join(dst_dir, file_name)

        # If the file is a regular file, check if it exists in the target directory.
        if os.path.isfile(src_file_path):
            if not os.path.exists(dst_file_path):
                # If the file doesn't exist in the target directory, copy it over.
                log.info(f'Copying {src_file_path} to {dst_file_path}')
                with open(src_file_path, 'rb') as src_f:
                    content = src_f.read()
                    with open(dst_file_path, 'wb') as dst_f:
                        dst_f.write(content)
            elif not compare_files(src_file_path, dst_file_path):
                # If the file exists in the target directory but is different, update it.
                log.info(f'Updating {dst_file_path} with {src_file_path}')
                with open(src_file_path, 'rb') as src_f:
                    content = src_f.read()
                    with open(dst_file_path, 'wb') as dst_f:
                        dst_f.write(content)
            # If the file exists in the target directory and is the same, log it as up to date.
            else:
                log.debug(f'{dst_file_path} is up to date')
        # If the file is a directory, recursively synchronize its contents.
        elif os.path.isdir(src_file_path):
            if not os.path.exists(dst_file_path):
            # If the directory doesn't exist in the target directory, create it.
                log.info(f'Creating directory {dst_file_path}')
                os.mkdir(dst_file_path)
            sync(src_file_path, dst_file_path)
    for file_name in os.listdir(dst_dir):
        src_file_path = os.path.join(src_dir, file_name)
        dst_file_path = os.path.join(dst_dir, file_name)
        if os.path.isfile(dst_file_path) and not os.path.exists(src_file_path):
            log.info(f'Removing {dst_file_path}')
            os.remove(dst_file_path)
        elif os.path.isdir(dst_file_path) and not os.path.exists(src_file_path):
            log.info(f'Removing directory {dst_file_path}')
            os.rmdir(dst_file_path)

if __name__ == '__main__':
    args = get_args()
    logging.basicConfig(filename=args.log, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    while True:
        sync(args.src, args.dst)
        time.sleep(args.interval)
