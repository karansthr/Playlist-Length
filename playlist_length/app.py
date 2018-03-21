import json
import os
import sys
import subprocess as sp

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
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('I found no duration')
    # return None


def main():
    if len(sys.argv) == 1:
        print("please give path to a directory")
        exit()
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(
            "give the directory path as an argument, use . for currect directory"
        )
        exit()
    item_list = os.listdir(directory)
    total_length_in_minute = 0
    for i in item_list:
        if os.path.isfile(i) and magic.from_file(
                i, mime=True).split('/')[0].lower() == "video":
            total_length_in_minute += duration(i) / 60
    print("Lenght of all vidoes in minutes :", int(1 + total_length_in_minute))


if __name__ == '__main__':
    main()
