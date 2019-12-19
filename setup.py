from setuptools import setup, find_packages

from __version__ import version

description = 'generate an application, as fast as possible'

setup(
    name='sfgen',
    version=version,
    packages=find_packages(),
    url='http://www.senaps.blog.ir',
    license='MIT',
    author='sneaps',
    author_email='gerdakan.sa@gmail.com',
    description=description,
        #TODO: entry points should be fixed with new style:))
    entry_points={
        'console_scripts': [
            'sfgen = sfgen.cli:main'
        ],
    }
)
