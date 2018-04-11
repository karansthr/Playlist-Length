from distutils.core import setup
from playlist_length.__version__ import __version__

requires = ('huepy==0.9.6', 'python-magic>=0.4.15', 'tqdm>=4.19.9')

setup(
    name='playlist-length',
    version=__version__,
    description='A command-line tool to get length of all videos in a directory',
    long_description=open('README.md').read().strip(),
    author='Karan Suthar',
    author_email='karansthr97@gmail.com',
    url='http://github.com/karansthr/playlist-length',
    packages=['playlist_length'],
    install_requires=requires,
    license='MIT License',
    keywords='videolength playlist-length',
    entry_points={
        'console_scripts': ['playlistlen=playlist_length.main:main'],
    },
)
