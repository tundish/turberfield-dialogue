.. _packaging:

Packaging
:::::::::

* Discovery
* Metadata search::

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

* Tighter constraints::

    def is_fully_cast(folder, references):
        for script in SceneScript.scripts(**folder._asdict())
            with script as dialogue:
                selection = dialogue.select(references)
                if all(selection.values()):
                    continue:
                else:
                    return False
        return True

::

    ~/py3.5/bin/python -c"import uuid; print(uuid.uuid4().hex)"

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
