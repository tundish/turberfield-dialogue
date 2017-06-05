..  Titling
    ##++::==~~--''``

API Reference
:::::::::::::

Data model
==========

.. autoclass:: turberfield.dialogue.model.Model

.. autoattribute:: turberfield.dialogue.model.Model.Shot
   :annotation: (name, scene, items)

.. autoattribute:: turberfield.dialogue.model.Model.Property
   :annotation: (entity, object, attr, val)

.. autoattribute:: turberfield.dialogue.model.Model.Audio
   :annotation: (package, resource, offset, duration, loop)

.. autoattribute:: turberfield.dialogue.model.Model.Memory
   :annotation: (subject, object, state, text, html)

.. autoattribute:: turberfield.dialogue.model.Model.Line
   :annotation: (persona, text, html)

Scene scripts
=============

.. autoattribute:: turberfield.dialogue.model.SceneScript.Folder
   :annotation: (pkg, description, metadata, paths, interludes)

.. autoclass:: turberfield.dialogue.model.SceneScript
   :members: scripts, read, select, cast, run
   :member-order: bysource
