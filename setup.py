from setuptools import setup

setup(
    name='pyreaqtive',
    version='0.1.0',
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
