from setuptools import setup

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
    packages=['pyreaqtive', 'pyreaqtive.models', 'pyreaqtive.widgets'],
    url='https://github.com/polfeliu/pyreaqtive',
    license='Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)',
    author='Pol Feliu Cuberes',
    author_email='feliupol@gmail.com',
    keywords='pyqt5 framework reactive gui',
    description='PyQt Reactive Framework',
    install_requires=[
        "pyqt5>=5.6"
    ]
)
