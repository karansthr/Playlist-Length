import hashlib
import os
import pickle


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.playlist_length')

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def pluralize(number, base, suffix):
    if number < 2:
        return '{} {}'.format(number, base)
    return '{} {}{}'.format(number, base, suffix)


class CacheUtil:
    def __init__(self, path):
        self.dir_path = os.path.abspath(path)
        self.cache = self._get_cached_data()

    @staticmethod
    def get_hash(string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def _get_cached_data(self):
        file_name = self.get_hash(self.dir_path)
        cache_file_path = os.path.join(CACHE_DIR, file_name)
        if not os.path.exists(cache_file_path):
            with open(os.path.join(CACHE_DIR, file_name), 'wb') as file:
                data = {}
                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open(cache_file_path, 'rb') as file:
                data = pickle.load(file)
        return data

    def save(self):
        file_name = self.get_hash(self.dir_path)
        cache_file_path = os.path.join(CACHE_DIR, file_name)
        with open(cache_file_path, 'wb') as file:
            pickle.dump(self.cache, file, protocol=pickle.HIGHEST_PROTOCOL)
