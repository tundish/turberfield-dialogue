..  Titling
    ##++::==~~--''``

Installation
::::::::::::

Install Python
==============

The version of Python you use depends on your Operating System. You should
run Turberfield in the most recent Python available for your OS. Two examples
are shown below:

* Virtual environment on `Linux or MacOSX`_ with Python 3.5 from a package repository.
* Virtual environment on `Microsoft Windows 8.1`_ with Python 3.6.1 downloaded from
  the Python website.


Create a Python virtual environment
===================================

Linux or MacOSX
~~~~~~~~~~~~~~~

#. Create a new Python virtual environment::

    $ python3.5 -m venv ~/py3.5

#. Upgrade your version of `pip`::

    $ ~/py3.5/bin/pip install --upgrade pip

Microsoft Windows 8.1
~~~~~~~~~~~~~~~~~~~~~

#.  Ensure the environment variable '`%USERPROFILE%`' points to your user directory.
#.  Download and install `Python 3.6.1 for Windows`_.
#.  Create a new Python virtual environment::

    > C:\Program Files (x86)\Python 3.6\python.exe -m venv %USERPROFILE%\py3.6

#.  Upgrade your version of `pip`::

    > %USERPROFILE%\py3.6\Scripts\pip install --upgrade pip

.. _install Turberfield Dialogue:

Install Turberfield Dialogue into the Python environment
========================================================

On Linux and MacOSX::

    $ ~/py3.5/bin/pip install turberfield-dialogue[audio]

On Windows 8.1::

    > %USERPROFILE%\py3.6\Scripts\pip install turberfield-dialogue[audio]

.. _PyPI: https://pypi.python.org/pypi
.. _Python 3.6.1 for Windows: https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe
