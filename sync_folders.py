import os, sys, logging, argparse
from hashlib import md5

def get_args():
    # Creating an ArgumentParser object
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, required=True,
                        help='Source directory to be synchronized')
    parser.add_argument('--dst', type=str, required=True,
                        help='Target directory to synchronize with')
    parser.add_argument('--interval', type=int, required=True,
                        help='Synchronization interval in seconds')
    parser.add_argument('--log', type=str, required=True,
                    help='Log file path')
    # Parsing the command line arguments
    args = parser.parse_args()

    # Creating the source and target directories if they don't exist
    for folder_name in [args.src, args.dst]:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f'Folder "{folder_name}" created successfully')
        else:
            continue
    return args

def compare_files(src_file_path, dst_file_path):
    if not os.path.exists(src_file_path):
        return False
    with open(src_file_path, 'rb') as src_f, open(dst_file_path, 'rb') as dst_f:
        return md5(src_f.read()).hexdigest() == md5(dst_f.read()).hexdigest()

def sync(src_dir, dst_dir):
    log = logging.getLogger('sync')
    for file_name in os.listdir(src_dir):
        src_file_path = os.path.join(src_dir, file_name)
        dst_file_path = os.path.join(dst_dir, file_name)
        if os.path.isfile(src_file_path):
            if not os.path.exists(dst_file_path):
                log.info(f'Copying {src_file_path} to {dst_file_path}')
                with open(src_file_path, 'rb') as src_f:
                    content = src_f.read()
                    with open(dst_file_path, 'wb') as dst_f:
                        dst_f.write(content)
            elif not compare_files(src_file_path, dst_file_path):
                log.info(f'Updating {dst_file_path} with {src_file_path}')
                with open(src_file_path, 'rb') as src_f:
                    content = src_f.read()
                    with open(dst_file_path, 'wb') as dst_f:
                        dst_f.write(content)
            else:
                log.debug(f'{dst_file_path} is up to date')
        elif os.path.isdir(src_file_path):
            if not os.path.exists(dst_file_path):
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
