import os
from distutils.core import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        os.system('sudo apt-get install ffmpeg')
        install.run(self)


setup(
    name='playlist-length',
    version='1.0',
    description='A simple tool to get total lenght of videos in a directory',
    long_description=open('README.md').read().strip(),
    author='Karan Suthar',
    author_email='karansthr97@gmail.com',
    url='http://github.com/karansthr/playlist-length',
    packages=['playlist_length'],
    install_requires=["python-magic"],
    license='MIT License',
    cmdclass={'install': CustomInstallCommand},
    keywords='videolenght playlist-length',
    entry_points={
        'console_scripts': ['playlistlen=playlist_length:main'],
    }
)
