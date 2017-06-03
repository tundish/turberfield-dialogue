..  Titling
    ##++::==~~--''``

Installation
::::::::::::

Install Python
==============

The version of Python you're going to use depends on your Operating System.
Two examples are documented below:

* An environment on `Linux or MacOSX`_ with Python 3.5 installed from a package repository.
* An environment on `Microsoft Windows 8.1`_ with Python 3.6.1 downloaded from
  the Python website.

You should run Turberfield in the most recent Python available for your OS. If you find
a more recent version than is shown here, then do pick that.

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

.. admonition:: What's pip?

   When you first install Python, it comes with only a small number of programs
   to run.

   `Pip` installs packages. That is, programs and libraries. Turberfield is
   one such library. There are many thousands more. A community of developers
   puts them on the internet for all to use.

   When you invoke `pip` like this, it goes out to the internet to find the package
   you want. It downloads it and installs it to your Python environment.

   You can also tell `pip` how much of a package to install. If that package does
   many things, you can limit it to one particular job, or install everything it
   is capable of doing.

   In a moment, we will install `turberfield-dialogue`, including all its `audio`
   capabilities. 

.. _install Turberfield Dialogue:

Install Turberfield Dialogue into the Python environment
========================================================

On Linux and MacOSX::

    $ ~/py3.5/bin/pip install turberfield-dialogue[audio]

On Windows 8.1::

    > %USERPROFILE%\py3.6\Scripts\pip install turberfield-dialogue[audio]

.. _PyPI: https://pypi.python.org/pypi
.. _Python 3.6.1 for Windows: https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe