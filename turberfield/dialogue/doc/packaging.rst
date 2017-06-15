..  Titling
    ##++::==~~--''``

.. _publishing:

Publishing
::::::::::

The demo examples you've seen so far were arranged as standalone
directories containing a Python module and some scene script files.

You can get started quickly by working this way, but before your
screenplay is ready, you need to have properly configured it as
a Python package.

Packaging gives you the following advantages:

* Versioning_
* Attribution_
* Distribution_
* Installability_
* `Dependency management`_
* Discoverability_

Checklist
=========

Turning your screenplay into a package might be a pain the first time
you do it. But you'll reap the benefits after that. Here's what you have
to do.

#. `Organise your project directory`_
#. `Make a manifest`_
#. `Write a README file`_
#. `Write the setup.py`_

Organise your project directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose your screenplay, **mydrama** is in a single directory of that name.
You have three scene script files; `begin.rst`, `middle.rst`, and `end.rst`.
You have an idea for a soundtrack you call `theme.wav`. And there is one
Python module called `logic.py`. You have saved some options as a file
called `rehearse.cli`::

    mydrama
    ├── begin.rst
    ├── middle.rst
    ├── end.rst
    ├── theme.wav
    ├── logic.py
    └── rehearse.cli

Now create four more empty files as follows::

    ├── __init__.py
    ├── MANIFEST.in
    ├── README.rst
    └── setup.py

There is nothing more to do to `__init__.py`. It stays empty. We will deal
with the other three in turn.

.. important::

   The naming conventions for Python packages are quite strict. You should
   use only lower case letters. If you want to signify a space in the directory
   name, use an underscore.

Make a manifest
~~~~~~~~~~~~~~~

The `MANIFEST.in` file decides which of your source files get
installed. It can filter out any project files created by your text
editor, cache files and the like. It should look like this::

    recursive-include . *.cli
    recursive-include . *.rst
    recursive-include . *.wav

Write a README file
~~~~~~~~~~~~~~~~~~~

The `README.rst` file is an opportunity to describe your drama to
potential collaborators. It is a reStructuredText_ file, so you can include
hyperlinks and other useful structures.

At a minimum, this file should contain your name, email address and
an assertion of your copyright. Other details are up to you.

Write the setup.py
~~~~~~~~~~~~~~~~~~

`setup.py` is like an electronic form which tells the packaging system
everything about your project. Here is the standard boilerplate you should use.

.. code-block:: python

    #!/usr/bin/env python
    # encoding: UTF-8

    from setuptools import setup
    import os.path

    __doc__ = open(
        os.path.join(os.path.dirname(__file__), "README.rst"),
        "r"
    ).read()

    setup(
        name="mydrama",
        version="0.1.0",
        description="A dramatic screenplay",
        author="Ernest Scribbler",
        author_email="escribbler@zmail.com",
        url="http://pypi.python.org/pypi/mydrama",
        long_description=__doc__,
        classifiers=[
            "Framework :: Turberfield",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: Other/Proprietary License",
        ],
        packages=["mydrama"],
        package_dir={"mydrama": "."},
        include_package_data=True,
        install_requires=["turberfield-dialogue"],
        zip_safe=True,
    )

Of course, you'll need to alter some details to match the name of your
particular project, here::

        name="mydrama",

... and here::

        packages=["mydrama"],
        package_dir={"mydrama": "."},

In the next few sections, we'll customise a little further.

Versioning
==========

As soon as other people begin to use your dialogue, you'll need to give
them a way of deciding whether they want to use your latest rewrite or
to stick with an earlier revision. Every release of your work will have a
version number to identify it.

You declare the version in the `setup` parameters in `setup.py`::

    version="0.1.0",

The three digits reflect the significance of any new change:

    * Trivial fixes increment the rightmost digit.
    * Significant changes increment the middle version field. This is the
      most frequent case; the number can go as high as you like, even into
      the hundreds.
    * Major changes which are incompatible with previous versions require
      an increment to the leftmost digit. 

Attribution
===========

I'm guessing your name is not Ernest Scribbler. If it is, write in
and let me know! Otherwise, you'll change the following parameters to match
your online identity::

    author="Ernest Scribbler",
    author_email="escribbler@zmail.com",

Distribution
============

The command to create a `distribution` of your project is this::

    ~py3.5/bin/python setup.py sdist

The packaging system creates an installable for you. You'll find
it at `dist/mydrama-0.1.0.tar.gz` (or `.zip`, depending on your OS).

You can upload that file to a package repository. The most popular is
PyPI_ but there are alternatives, such as Gemfury_.

So you'll need to declare the correct URL to your package once
it gets up there::

        url="http://pypi.python.org/pypi/mydrama",

This is a bit of a chicken-and-egg situation of course. You'll have to
anticipate what the URL is going to be before you upload it, or
else you'll have an error in the first release which you'll need to fix
afterwards. 

Installability
==============

With your work properly packaged, you can be confident that others can
start using it with a minimum of fuss.

If you upload it to PyPI_, `pip` will go out and fetch it::

    ~/py3.5/bin/pip install mydrama 

Or you could send your package file by email or on a USB stick. Then
the install command targets the package file like this::

    ~/py3.5/bin/pip install mydrama-0.1.0.tar.gz

Dependency management
=====================

Your package gets to declare which other Python libraries it needs to run.
I already gave you the one essential dependency::

    install_requires=["turberfield-dialogue"],

It's quite possible that your `logic.py` might rely on some other
library to do a particular job. Perhaps you've written a role for a banker
who needs to `calculate loan interest`_.

Whatever PyPI_ package you add to this list will be automatically installed
with your screenplay and available for use from your Python modules.

Discoverability
===============

Create a unique global id for your work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not only do you get to declare your authorship and copyright, but you
also declare a global id for your work.::

    ~/py3.5/bin/python -c"import uuid; print(uuid.uuid4().hex)"

When you create a `setup.py` for your installable package, you can decide
whether to advertise through these two interfaces:

**turberfield.interfaces.folder**
    For :py:class:`~turberfield.dialogue.model.SceneScript.Folder` objects.
**turberfield.interfaces.references**
    For :py:class:`~turberfield.dialogue.model.SceneScript.Folder` objects.

If you've not yet done so, you should follow the `packaging tutorials`_
I recommended earlier on. There are three of them, and they take about
half an hour each.

Both demo examples are also supplied in packaged form:

    Battle Royal
        turberfield/dialogue/sequences/battle

        The turberfield-dialogue package declares the scene script
        folder as discoverable via the `turberfield.interfaces.folder`
        interface.

    Cloak of Darkness
        turberfield/dialogue/sequences/cloak

Global identity
===============

::

    entry_points={
        "console_scripts": [
            "addisonarches = addisonarches.main:run",
            "addisonarches-web = addisonarches.web.main:run",
        ],
        "turberfield.interfaces.sequence": [
            "stripeyhole = addisonarches.sequences.stripeyhole:contents",
        ],
        "turberfield.interfaces.ensemble": [
            "sequence_01 = addisonarches.scenario.common:ensemble",
        ],
    },
    zip_safe=False

Performing
::::::::::

Making a name for yourself
==========================

Absolute paths.

Constraining entity selection
=============================

::

    def is_fully_cast(folder, references):
        for script in SceneScript.scripts(**folder._asdict())
            with script as dialogue:
                selection = dialogue.select(references)
                if all(selection.values()):
                    continue:
                else:
                    return False
        return True

Using Metadata
==============

::

    from turberfield.utils.misc import gather_installed
    guid, folder = next(
        k, v
        for k, v in dict(
            gather_installed("turberfield.interfaces.folder")
        ).items()
        if "betrayal" in v.metadata,
    )

    references = dict(
        gather_installed("turberfield.interfaces.references")
    ).get(guid)

.. _packaging tutorials: http://thuswise.co.uk/packaging-python-for-scale-part-one.html
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _PyPI: https://pypi.python.org/pypi
.. _Gemfury: https://gemfury.com
.. _calculate loan interest: https://pypi.python.org/pypi/tallywallet-common
