playlist-len

### Installation

hip up your terminal and type following command

```pip install --user -e git+https://github.com/karansthr/playlist-length#egg=playlist-length```

if your ~/.local/bin/ is not in PATH then run ```$ export PATH=$PATH:${HOME}/.local/bin/```
you may add above line of code in ~/.zshrc or ~/.bashrc etc. to repeat above step every time a terminal is opened.

then use following command to get length of all the videos in a directory 

```playlistlen path_to_directory```

for example <br>
```playlistlen .```

above command will give length of all the available videos in current directory in minutes. 
