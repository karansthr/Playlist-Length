from setuptools import setup

from playlist_length.__version__ import __version__


requires = (
    'huepy==0.9.6',
    'python-magic>=0.4.15',
    'tqdm>=4.19.9',
    'futures;python_version<"3.4"',
)

setup(
    name='playlist-length',
    version=__version__,
    description='A command-line tool to get length of all videos in a directory',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
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
    project_urls={
        'Bug Reports': 'https://github.com/karansthr/playlist-length/issues',
        'Source': 'https://github.com/karansthr/playlist-length/',
        'Blog': 'https://fosstack.com/tips/videos-playlist-length-calculator/',
        'About': 'https://fosstack.com/about/'
    }
)
