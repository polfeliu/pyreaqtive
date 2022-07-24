# pyreaqtive
[![Docs](https://readthedocs.org/projects/pyreaqtive/badge/?style=flat)](https://pyreaqtive.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/pyreaqtive)](https://pypi.org/project/pyreaqtive/)
[![Pipeline](https://img.shields.io/github/workflow/status/polfeliu/pyreaqtive/Pipeline/master)](https://github.com/polfeliu/pyreaqtive/actions/workflows/push.yml)
[![Mypy](https://img.shields.io/badge/-mypy-brightgreen)](https://github.com/polfeliu/pyreaqtive/actions/workflows/push.yml)
[![License](https://img.shields.io/pypi/l/pyreaqtive)](https://raw.githubusercontent.com/polfeliu/pyreaqtive/master/LICENSE)
![Logo](https://raw.githubusercontent.com/polfeliu/pyreaqtive/master/doc/source/_static/logo256.png)

pyreaqtive is a framework for developing applications in pyqt/pyside with reactive programming. It enables to write applications in a declarative form, that is focused on data and functionality and that does not bloat code with gui callbacks.

The library provides several models to hold data, and many prebuilt widgets and layouts to present the data from the models to the user, making the separation from data and visualization, and the adequate link between them, a simple task.

All reactive widgets and layouts use qt built-in widgets, which makes them fully compatible with qt without loosing functionality. Reactive and non-reactive parts can be mixed into an application, and non-reactive components can be turned to reactive ones without necessarily changing codebases.

It was originally developed for PyQt5, but through the QtPy package it is also compatible with to PyQt6, PySide2 and PySide6.

## Documentation
https://pyreaqtive.readthedocs.io/en/latest/
