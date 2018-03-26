# Playlist Length

A command-line tool to calculation the length of all the vidoes in a directory

## Prerequisites

**ffmpeg** package is required for this package to work, so you need to get it installed on your system

## Installing
hit up your terminal and type following command

```
$ pip install --user -e git+https://github.com/karansthr/playlist-length#egg=playlist-length
```

if your ~/.local/bin/ is not in PATH then run ```$ export PATH=$PATH:${HOME}/.local/bin/``` <br>
you may add above line of code in ~/.zshrc or ~/.bashrc etc. to repeat above step every time a terminal is opened.

then use following command to get length of all the videos in a directory
```
$ playlistlen -p path_to_directory
```

or use following command for current directory
```
$ playlistlen
```

By default it will look for subdirectories in the given directory, if you want it to look for only files in the given directory only, then use **--no-subdir** flag, for example 
```
$ playlistlen -p path_to_directory --no-subdir
```

for help use -h or --help, for example
```
$ playlistlen --help
```

## Authors

* **Karan Suthar** (https://github.com/karansthr)
* **Mohit Solanki** (https://github.com/mohi7solanki)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
