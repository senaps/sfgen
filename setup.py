from distutils.core import setup, , find_packages


setup(
    name='sfgen',
    version='0.0.1dev',
    packages=find_packages(),
    url='http://www.senaps.blog.ir',
    license='MIT',
    author='sneaps',
    author_email='gerdakan.sa@gmail.com',
    description='generate a flask application, as fast as possible',
    entry_points={
        'console_scripts': [
            'sfgen = src.cli:main'
        ],
    }
)
