..  Titling
    ##++::==~~--''``

API Reference
:::::::::::::

This API gives you a `single function`_ for creating a performance from a
:py:class:~`turberfield.dialogue.model.SceneScript.Folder`
of Turberfield dialogue. You can modify how this performance is presented
in your game by customising or replacing a handler_ function which processes
events_ from the scene script files.

The `scene scripts`_ themselves also have an API, allowing you to interact with
the process by which entities are selected and cast to roles.

Events
======

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

Handler
=======

.. autoclass:: turberfield.dialogue.handlers.TerminalHandler
   :members: handle_audio, handle_interlude, handle_line, handle_memory, handle_property, handle_scene, handle_scenescript, handle_shot
   :member-order: bysource

Players
=======

.. autofunction:: turberfield.dialogue.player.rehearse

.. _single function: py:func:`turberfield.dialogue.player.rehearse`.
