# -*- coding: utf-8 -*-

import argparse
import os
import subprocess as sp
import sys
import re
from concurrent.futures import as_completed, ProcessPoolExecutor

import magic
from huepy import bold, green, red
from tqdm import tqdm

from .utils import pluralize
from .__version__ import __version__


DURATION_REGEX = re.compile(r'duration=(.*)')

REGEX_MAP = {
    'video': re.compile(r'video|Video'),
    'audio': re.compile(r'audio|Audio'),
    'audio/video': re.compile(r'audio|video|Audio|Video'),
}


def duration(file_path):
    """
    Return the duration of the the file in minutes.
    """
    command = ["ffprobe", "-show_entries", "format=duration", "-i", file_path]
    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, error = pipe.communicate()
    match_object = None if error else DURATION_REGEX.search(out.decode('utf-8'))
    if match_object is None:
        return 0
    length = float(match_object.group(1)) / 60
    return length


def is_media_file(file_path):
    try:
        match_object = media_type.match(magic.from_file(file_path, mime=True))  # noqa
        if match_object is not None:
            return file_path
    except IOError:
        # Probably this directory contains some file/folder that the
        # user don't have permission to read or maybe it is a symlinked
        # file.
        pass


def get_all_files(BASE_PATH, no_subdir):

    def with_subdir():
        return (
            os.path.join(root, file)
            for root, _, files in os.walk(BASE_PATH)
            for file in files
            if file[0] != '.'
        )

    def without_subdir():
        for file in os.listdir(BASE_PATH):
            file_path = os.path.join(BASE_PATH, file)
            if os.path.isfile(file_path) and not os.path.islink(file_path):
                yield file_path

    all_files = without_subdir() if no_subdir else with_subdir()
    return list(all_files)


def calculate_length(BASE_PATH, no_subdir, media_type):
    if not os.path.isdir(BASE_PATH):
        return bold(red('Error: This doesn\'t seem to be a valid directory.'))

    all_files = get_all_files(BASE_PATH, no_subdir)

    with ProcessPoolExecutor() as executor:
        sys.stdout.write('\n')
        video_files = []
        tasks = [executor.submit(is_media_file, file_path) for file_path in all_files]

        for task in tqdm(
            as_completed(tasks), total=len(tasks), desc='Filtering {}'.format(media_type)
        ):
            path = task.result()
            if path is not None:
                video_files.append(path)

    if not video_files:
        return bold(red('Seems like there are no {} files. ¯\_(ツ)_/¯'.format(media_type)))

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
        minutes_string = pluralize(length, base='minute', suffix='s')
        result = 'Length of all {} is {}.'.format(media_type, minutes_string)
    else:
        hours, minutes = divmod(length, 60)
        hours_string = pluralize(hours, base='hour', suffix='s')
        minutes_string = pluralize(minutes, base='minute', suffix='s')
        result = 'Length of all {} is {} and {}.'.format(
            media_type, hours_string, minutes_string
        )
    return bold(green(result))


def get_parser():
    parser = argparse.ArgumentParser(
        description='''
        Output the total duration of all the audio and video files in the given directory.
        '''
    )
    parser.add_argument(
        'path',
        help='Path to a directory. Defaults to current directory',
        type=str,
        nargs='?',
        default='.',
    )
    parser.add_argument(
        '--no-subdir',
        help='Don\'t look for videos in sub directories.',
        action='store_true',
    )
    parser.add_argument(
        '--media-type',
        help='Type of media file to you want to check.',
        type=str,
        choices=['audio', 'video', 'both'],
        default='video',
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
    )
    return parser


def main():
    try:
        parser = get_parser()
        args = parser.parse_args()
        if args.media_type == 'both':
            args.media_type = 'audio/video'
        # why pass every time to `is_media_file` inject to globals intead ;)
        globals()['media_type'] = REGEX_MAP[args.media_type]
        result = calculate_length(args.path, args.no_subdir, args.media_type)
    except (KeyboardInterrupt, SystemExit):
        sys.stdout.write('\nPlease Wait... Exiting Gracefully!\n')
    else:
        sys.stdout.write('\n{}\n\n'.format(result))
    finally:
        sys.exit()
