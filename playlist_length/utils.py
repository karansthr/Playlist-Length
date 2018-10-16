import hashlib
import os
import pickle


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.playlist_length')
os.makedirs(CACHE_DIR, exist_ok=True)


def pluralize(number, base, suffix):
    if number < 2:
        return '{} {}'.format(number, base)
    return '{} {}{}'.format(number, base, suffix)


class CacheUtil:
    def __init__(self, path, media_type):
        self.media_type = media_type
        self.dir_path = os.path.abspath(path)
        self.cache_file_path = self._get_cache_file_path()
        self.cache = self._get_cached_data()

    @staticmethod
    def get_hash(string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()

    def _get_cache_file_path(self):
        file_name = self.get_hash(self.dir_path + self.media_type)
        cache_file_path = os.path.join(CACHE_DIR, file_name)
        return cache_file_path

    def _get_cached_data(self):
        if not os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, 'wb') as file:
                data = {}
                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open(self.cache_file_path, 'rb') as file:
                data = pickle.load(file)
        return data

    def save(self):
        with open(self.cache_file_path, 'wb') as file:
            pickle.dump(self.cache, file, protocol=pickle.HIGHEST_PROTOCOL)
