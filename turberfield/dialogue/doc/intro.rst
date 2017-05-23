..  Titling
    ##++::==~~--''``

Overview
::::::::


So, you're a writer?
====================

Turberfield-dialogue is a framework which supports screenwriting.
It defines a format for scripts which feels familiar to writing practitioners.
Its design uses terminology from the screenplay tradition.

* Folders contain sequences of action.
* Scripts separate action into scenes.
* Scenes are made up of shots.
* Shots can contain lines of dialogue or audio effects.

Turberfield comes with a rehearsal tool which lets you run through your dialogue and fine-tune
your tone and pace.

We'll go over the syntax of Turberfield scene files in a moment.
It is based on a system called reStructuredText_. That's the same system which generated
the pages you are reading now.

As well as producing dialogue, you may be called upon to define some game logic too.
The Turberfield framework encourages you to write game logic in Python_.
Don't worry, it's the friendliest programming language I know...

So, you're a developer.
=======================

If you have written no code at all yet, Turberfield by itself can provide
all you need for an early prototype.

Or, you can use it as a library to provide a dialogue system for your existing Python game.

Python is also your publisher. When it's time to collaborate with others or show your dialogue
to an audience, you'll use the Python packaging system to distribute and install your work.

By the end of the creative process, you will need some familiarity with
`packaging techniques`_. That's not usually a subject for beginners, so I wrote this
`easy tutorial`_. If you revisit this topic from time to time, you should have
learned what you need by the time your dialogue is ready to share. 

.. _Python: http://python.org
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _packaging techniques: https://packaging.python.org/distributing/
.. _easy tutorial: http://thuswise.co.uk/packaging-python-for-scale-part-one.html