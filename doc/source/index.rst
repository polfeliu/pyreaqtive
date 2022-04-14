.. pyreaqtive documentation master file, created by

Welcome to pyreaqtive's documentation!
======================================

.. image:: _static/logo512.png
   :width: 200
   :align: center

pyreaqtive is a framework for developing applications in pyqt/pyside with reactive programming. It enables to write applications in a declarative form, that is focused on data and functionality and that does not bloat code with gui callbacks.

The library provides several models to hold data, and many prebuilt widgets and layouts to present the data from the models to the user, making the separation from data and visualization, and the adequate link between them, a simple task.

All reactive widgets and layouts use qt built-in widgets, which makes them fully compatible with qt without loosing functionality. Reactive and non-reactive parts can be mixed into an application, and non-reactive components can be turned to reactive ones without necessarily changing codebases.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   examples/examples

   api/models
   api/widgets
   api/layouts
   api/rq_getattr
   api/rq_getlist
   api/rq_connect
   api/rq_async

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
