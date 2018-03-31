import argparse
import glob
import json
import os
import subprocess as sp
import sys
from concurrent.futures import as_completed, ProcessPoolExecutor

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
        return json.loads(out.decode('utf-8'))


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
    if 'video' in magic.from_file(file_path, mime=True).lower():
        return file_path


def get_all_files(BASE_PATH, no_subdir):

    def with_subdir():
        for root, _, files in os.walk(BASE_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                if not os.path.islink(file_path) and not file.startswith('.'):
                    yield file_path

    def without_subdir():
        return filter(os.path.isfile, glob.glob(os.path.join(BASE_PATH, '*.*')))

    if no_subdir:
        return without_subdir()

    return with_subdir()


def video_len_calculator(BASE_PATH, no_subdir):
    if not os.path.isdir(BASE_PATH):
        return bold(red('Error: This doesn\'t seem to be a valid directory.'))

    all_files = list(get_all_files(BASE_PATH, no_subdir))

    with ProcessPoolExecutor() as executor:
        sys.stdout.write('\n')
        video_files = []
        tasks = [executor.submit(is_video_file, file_path) for file_path in all_files]

        for task in tqdm(
            as_completed(tasks), total=len(tasks), desc='Filtering videos'
        ):
            path = task.result()
            if path is not None:
                video_files.append(path)

    if not video_files:
        return bold(red('Seems like there is no video file. ¯\_(ツ)_/¯'))

    with ProcessPoolExecutor() as executor:
        sys.stdout.write('\n')
        result = list(
            tqdm(
                executor.map(duration, video_files),
                total=len(video_files),
                desc='Calculating time',
            )
        )

    length = round(sum(result))

    if length < 60:
        result = 'Length of all vidoes is {} minutes.'.format(length)
    else:
        hours, minutes = divmod(length, 60)
        result = 'Length of all videos is {} hours and {} minutes.'.format(
            hours, minutes
        )
    return bold(green(result))


def main():
    parser = argparse.ArgumentParser(
        description='''
        Output the total duration of all the videos in given directory.
        '''
    )
    parser.add_argument(
        '-p',
        '--path',
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
    result = video_len_calculator(args.path, args.no_subdir)
    sys.stdout.write('\n{}\n\n'.format(result))


if __name__ == '__main__':
    main()
