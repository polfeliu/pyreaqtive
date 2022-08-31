from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
from pyreaqtive import __version__

setup(
    name='pyreaqtive',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    packages=find_packages(include=["pyreaqtive", "pyreaqtive.*"]),
    package_data={'pyreaqtive': ['py.typed']},
    url='https://github.com/polfeliu/pyreaqtive',
    license='Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)',
    author='Pol Feliu Cuberes',
    author_email='feliupol@gmail.com',
    keywords='pyqt5 framework reactive gui',
    description='PyQt Reactive Framework',
    install_requires=[
        "qtpy>2.0.0"
    ]
)
