..  Titling
    ##++::==~~--''``

.. _publishing:

Publishing
::::::::::

The demo examples you've seen so far have been presented as standalone
directories containing a Python module and some scene script files.

You can get started quickly by working this way, but before your
screenplay is ready, you need to have properly configured it as
a Python package.

Packaging
=========

Packaging gives you the following advantages:

* Attribution_
* Versioning_
* Deployment
* Distribution_
* Discoverability
* Dependency management
* Aggregation

Checklist
~~~~~~~~~

#. `Directory structure`_
#. `Create a manifest`_
#. `Create a README file`_
#. `Create the setup.py`_

Directory structure
-------------------

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

Create a manifest
-----------------

The `MANIFEST.in` file controls which of your source files get
installed. It can filter out any project files created by your text
editor, cache files and the like. It should look like this::

    recursive-include . *.cli
    recursive-include . *.rst
    recursive-include . *.wav

Create a README file
--------------------

The `README.rst` file is your first opportunity to describe your drama to
potential collaborators. It is a reStructuredText_ file, so you can include
hyperlinks and other useful structures.

At a minimum, this file should contain your name, email address and
an assertion of your copyright. Other details are up to you.

Create the setup.py
-------------------

`setup.py` file contains the packaging boilerplate.

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



Attribution
~~~~~~~~~~~


Create a unique global id for your work
---------------------------------------

Not only do you get to declare your autthorship and copyright, but you
also declare a global id for your work.::

    ~/py3.5/bin/python -c"import uuid; print(uuid.uuid4().hex)"

Versioning
~~~~~~~~~~

As soon as other people begin to use your dialogue, you'll need to give
them a way of deciding whether they want to use your latest rewrite or
to stick with an earlier revision. Every release of your work will have a
version number to identify it.

You define a version by creating an `__init__.py` file in your package
directory and making an entry like this::

    __version__ = "0.1.0"

Deployment
~~~~~~~~~~

A `manifest` file will control which of your source files get
installed. This will filter out any project files created by your text
editor, cache files and the like.::
 
    recursive-include . *.cli
    recursive-include . *.rst
    recursive-include . *.wav

Distribution
~~~~~~~~~~~~

With your work properly packaged, you can make it available to others
to download and install via PyPI_ or Gemfury_.

Discoverability
~~~~~~~~~~~~~~~

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
.. _PyPI: https://pypi.python.org/pypi
.. _Gemfury: https://gemfury.com
