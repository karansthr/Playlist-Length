# For unix
CACHE_PATH = '/tmp/.playlistlen_cache'

# Cache limit
LIMIT_CACHE = 100

BUF_SIZE = 65536


def get_file_mode():
    import os
    if os.path.exists(CACHE_PATH):
        mode_file = 'a'    # append if already exists
    else:
        mode_file = 'w'    # make a new file if not

    return mode_file


def find_in_cache(hash_file):
    try:
        with open(CACHE_PATH, 'r') as f:
            for line in f:
                line = line.rstrip()
                if hash_file in line:
                    return line
            return None
    except FileNotFoundError:
        return None


def hash_file_names(all_files):
    import hashlib
    md5 = hashlib.md5()
    md5.update(str(all_files).encode())
    return md5.hexdigest()


def add_cache(h_file, length):
    try:
        with open(CACHE_PATH, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    with open(CACHE_PATH, get_file_mode()) as f:
        if len(lines) >= LIMIT_CACHE:
            f.write('\n'.join(lines[1:]))
        f.write('{},{}\n'.format(h_file, length))
        return length


def find_or_add_cache(all_files, func):
    h_file = hash_file_names(all_files)
    c_file = find_in_cache(h_file)
    c_hit = False

    if c_file:
        c_hit = True
        result = c_file.split(',')[1]
    else:
        result = func(all_files)
        add_cache(h_file, result)
    return float(result), c_hit
