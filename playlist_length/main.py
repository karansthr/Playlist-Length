import argparse
import json
import os
import subprocess as sp
from concurrent.futures import ProcessPoolExecutor

import huepy
import magic
from tqdm import tqdm


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
    out, error = pipe.communicate()
    if not error:
        return json.loads(out)


def duration(vid_file_path):
    ''' Video's duration in seconds, return a float number.'''
    _json = probe(vid_file_path)
    if not _json:
        length = 0
    elif 'format' in _json:
        if 'duration' in _json['format']:
            length = float(_json['format']['duration']) / 60
    elif 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                length = float(s['duration']) / 60
                break
    return length


def is_video_file(file_path):
    if 'video' in magic.from_file(file_path, mime=True).lower():
        return file_path


def main(BASE_PATH):
    if not os.path.isdir(BASE_PATH):
        return(
            huepy.bold(
                huepy.red(
                    '\nError: This doesn\'t seem to be a valid directory.\n'
                )
            )
        )

    all_files = (
        os.path.join(root, file)
        for root, _, files in os.walk(BASE_PATH)
        for file in files
    )

    with ProcessPoolExecutor() as executor:
        video_files = list(
            filter(None, executor.map(is_video_file, all_files))
        )

    if not video_files:
        return huepy.bold(
            huepy.red('\nSeems like there is no video files. ¯\_(ツ)_/¯\n')
        )

    with ProcessPoolExecutor() as executor:
        print()
        result = list(
            tqdm(
                executor.map(duration, video_files),
                total=len(video_files),
                ascii=True,
                desc='Please Wait',
            )
        )
    length = round(sum(result))

    if length < 60:
        message = 'Length of all vidoes is {} minutes.'.format(length)
    else:
        hours, minutes = divmod(length, 60)
        message = 'Length of all vidoes is {} hours and {} minutes.'.format(
            hours, minutes
        )
    message = huepy.bold(huepy.green(message))
    return f'\n{message}\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''
        Output the total duration of all the videos in given directory.
        ''',
        usage='playlist-lentgh [-h] [-p/--path PATH]'
    )
    parser.add_argument(
        '-p', '--path',
        help='Path to a directory. Defaults to current directory',
        type=str,
        default='.',
    )

    args = parser.parse_args()
    BASE_PATH = args.path
    print(main(BASE_PATH))
