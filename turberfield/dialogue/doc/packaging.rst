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

Attribution
~~~~~~~~~~~

Create a `README.txt` file. 

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

Add a `MANIFEST.in` file to control which of your source files get
installed. This will filter out any project files created by your text
editor::
 
    include *.txt *.rst *.wav

Distribution
~~~~~~~~~~~~

With your work properly packaged, you can make it available to others
to download and install via PyPI_ or Gemfury_.

Make an empty `MANIFEST.in` file.

You'll need to create a `setup.py` file which contains the packaging
boilerplate.

.. code-block:: python

    #!/usr/bin/env python
    # encoding: UTF-8

    from distutils.core import setup
    import os.path

    __doc__ = open(os.path.join(os.path.dirname(__file__), "README.txt"),
                   "r").read()
    setup(
        name="inspyration",
        version="0.01",
        description="A simple MOTD program to illustrate packaging techniques",
        author="D Haynes",
        author_email="tundish@thuswise.org",
        url="http://pypi.python.org/pypi/inspyration",
        long_description=__doc__,
        classifiers=[
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
        ],
        py_modules=["inspyration"],
        scripts=["inspyration.py"]
    )

Discoverability
~~~~~~~~~~~~~~~

When you create a `setup.py` for your installable package, you can decide
whether to advertise through these two interfaces:

**turberfield.interfaces.folder**
    For :py:class:`~turberfield.dialogue.model.SceneScript.Folder` objects.
**turberfield.interfaces.references**
    For :py:class:`~turberfield.dialogue.model.SceneScript.Folder` objects.

::

    ~/py3.5/bin/python -c"import uuid; print(uuid.uuid4().hex)"

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
