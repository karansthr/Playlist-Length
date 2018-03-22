import json
import os
import sys
import subprocess as sp
from concurrent.futures import ProcessPoolExecutor

import magic


def probe(vid_file_path):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    if type(vid_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
        return

    command = [
        "ffprobe", "-loglevel", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", vid_file_path
    ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)


def duration(vid_file_path):
    ''' Video's duration in seconds, return a float number
    '''
    if video_file(vid_file_path):
        _json = probe(vid_file_path)

        if 'format' in _json:
            if 'duration' in _json['format']:
                return float(_json['format']['duration']) / 60

        if 'streams' in _json:
            # commonly stream 0 is the video
            for s in _json['streams']:
                if 'duration' in s:
                    return float(s['duration']) / 60
    # Maybe the file is not a valid video file
    return 0


def video_file(file_path):
    if (
        os.path.isfile(file_path) and
        magic.from_file(file_path, mime=True).split('/')[0].lower() == "video"
    ):
        return True
    return False


def main():
    if len(sys.argv) == 1:
        print("Please give path to a directory")
        exit()
    BASE_PATH = sys.argv[1]
    if not os.path.isdir(BASE_PATH):
        print(
            "Give the directory path as argument or use . for currect directory"
        )
        exit()
    all_files = os.listdir(BASE_PATH)
    with ProcessPoolExecutor() as executor:
        result = executor.map(
            duration, map(lambda x: os.path.join(BASE_PATH, x), all_files)
        )
    length = sum(result) + 1
    if length < 60:
        length = '{} minutes.'.format(int(length))
    else:
        hours, minutes = divmod(length, 60)
        length = '{} hours and {} minutes.'.format(int(hours), int(minutes))
    print('Length of all vidoes is {}'.format(length))


if __name__ == '__main__':
    main()
