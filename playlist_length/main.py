import argparse
import json
import os
import subprocess as sp
from concurrent.futures import ProcessPoolExecutor

import magic
from huepy import bold, green, red
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
            length = float(_json['format']['duration'])
    elif 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                length = float(s['duration'])
                break
    return length / 60


def is_video_file(file_path):
    if not os.path.islink(file_path) and 'video' in magic.from_file(
            file_path, mime=True).lower():
        return file_path


def get_files(BASE_PATH):
    for file in os.listdir(BASE_PATH):
        file_path = os.path.join(BASE_PATH, file)
        if os.path.isfile(file_path):
            yield file_path


def app(BASE_PATH, no_subdir):
    if not os.path.isdir(BASE_PATH):
        return(
            bold(red('\nError: This doesn\'t seem to be a valid directory.\n'))
        )

    if no_subdir:
        all_files = get_files(BASE_PATH)
    else:
        all_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(BASE_PATH)
            for file in files
        ]

    video_files = list(
        filter(is_video_file,
               tqdm(all_files, total=len(all_files), desc="Collecting vidoes")))

    if not video_files:
        return bold(red('\nSeems like there is no video files. ¯\_(ツ)_/¯\n'))

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
    message = bold(green(message))
    return '\n{}\n'.format(message)


def main():
    parser = argparse.ArgumentParser(
        description='''
        Output the total duration of all the videos in given directory.
        '''
    )
    parser.add_argument(
        '-p', '--path',
        help='Path to a directory. Defaults to current directory',
        type=str,
        default='.',
    )
    parser.add_argument(
        '--no-subdir',
        help='Don\'t look for videos in sub directories.',
        action='store_true',
    )
    args = parser.parse_args()
    print(app(args.path, args.no_subdir))

if __name__ == '__main__':
    main()
