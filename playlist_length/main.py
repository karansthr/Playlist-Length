import argparse
import json
import os
import subprocess as sp
from concurrent.futures import ProcessPoolExecutor

import huepy
import magic


def probe(vid_file_path):
    '''
    Give a json from ffprobe command line.

    @vid_file_path : The absolute (full) path of the video file, string.
    '''

    command = [
        'ffprobe',
        '-loglevel',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        vid_file_path,
    ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)


def duration(vid_file_path):
    ''' Video's duration in seconds, return a float number.'''
    if is_video_file(vid_file_path):
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


def is_video_file(file_path):
    return 'video' in magic.from_file(file_path, mime=True).lower()


def main():
    parser = argparse.ArgumentParser(
        description='''
        Output the total duration of all the videos in given directory.
        '''
    )
    parser.add_argument(
        '--path',
        help='Path to a directory. Defaults to current directory',
        type=str,
        default='.',
    )
    args = parser.parse_args()
    BASE_PATH = args.path

    if not os.path.isdir(BASE_PATH):
        print('Give the path to directory as an argument '\
              'or nothing for current directory.')
        exit()
    all_files = (
        os.path.join(root, file)
        for root, _, files in os.walk(BASE_PATH)
        for file in files
    )
    with ProcessPoolExecutor() as executor:
        result = executor.map(duration, all_files)
    length = round(sum(result))
    if not length:
        return huepy.bold(
            huepy.red('Seems like there is no video  ¯\_(ツ)_/¯')
        )
    if length < 60:
        message = 'Length of all vidoes is {} minutes.'.format(length)
    else:
        hours, minutes = divmod(length, 60)
        message = 'Length of all vidoes is {} hours and {} minutes.'.format(
            hours, minutes
        )
    message = huepy.bold(huepy.green(message))
    return message


if __name__ == '__main__':
    print(main())
