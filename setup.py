from distutils.core import setup


setup(
    name='playlist-length',
    version='1.3',
    description='A command-line tool to get length of all videos in a directory',
    long_description=open('README.md').read().strip(),
    author='Karan Suthar',
    author_email='karansthr97@gmail.com',
    url='http://github.com/karansthr/playlist-length',
    packages=['playlist_length'],
    install_requires=["python-magic", "tqdm", "huepy"],
    license='MIT License',
    keywords='videolength playlist-length',
    entry_points={
        'console_scripts': ['playlistlen=playlist_length.main:main'],
    },
)
