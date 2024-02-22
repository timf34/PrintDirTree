from setuptools import setup, find_packages

setup(
    name='dirtree',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dirtree=dirtree.__main__:main',
        ],
    },
    author='Tim Farrelly',
    author_email='timf34@gmail.com',
    description='A utility to print the directory tree structure with customizable exclusions.',
    install_requires=[
    ],
    python_requires='>=3.6',
)
