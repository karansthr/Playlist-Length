from distutils.core import setup


setup(
    name='playlist-length',
    version='1.1',
    description='A simple tool to get total lenght of videos in a directory',
    long_description=open('README.md').read().strip(),
    author='Karan Suthar',
    author_email='karansthr97@gmail.com',
    url='http://github.com/karansthr/playlist-length',
    packages=['playlist_length'],
    install_requires=["python-magic","tqdm","huepy"],
    license='MIT License',
    keywords='videolenght playlist-length',
    entry_points={
        'console_scripts': ['playlistlen=playlist_length:main'],
    }
)
