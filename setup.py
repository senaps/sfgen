from setuptools import setup, find_packages


setup(
    name='sfgen',
    version='1.0.0',
    packages=find_packages(),
    url='http://www.senaps.blog.ir',
    license='MIT',
    author='sneaps',
    author_email='gerdakan.sa@gmail.com',
    description='generate an application, as fast as possible',
    install_requires=[
            'click',
            'requests',
        ],
    entry_points={
        'console_scripts': [
            'sfgen = sfgen.cli:cli'
        ],
    }
)
