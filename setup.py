from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='printdirtree',
    version='0.1.4',
    packages=find_packages(),
    url="https://github.com/timf34/PrintDirTree",
    entry_points={
        'console_scripts': [
            'printdirtree=printdirtree.__main__:main',
        ],
    },
    author='Tim Farrelly',
    author_email='timf34@gmail.com',
    description='A CLI utility to print the directory tree structure with customizable exclusions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pyperclip',
    ],
    python_requires='>=3.6',
)
