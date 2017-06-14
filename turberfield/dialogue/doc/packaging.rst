..  Titling
    ##++::==~~--''``

.. _publishing:

Publishing
::::::::::

The demo examples you've seen so far have been presented as standalone
directories containing a Python module and some scene script files.

While you can get started quickly by working this way, before your
screenplay is ready, you need to have properly configured it as
a Python package.

Packaging
=========

Packaging gives you the following advantages:

* Versioning_
* Distribution
* Discoverability
* Dependency management
* Aggregation

Versioning
~~~~~~~~~~

As soon as other people begin to use your dialogue, you'll need to give
them a way of deciding whether they want to use your latest rewrite or
stick with an earlier revision. Every release of your work will have a
version number to identify it.

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
