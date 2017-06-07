..  Titling
    ##++::==~~--''``

.. _syntax:

Syntax guide
::::::::::::

Naming convention
=================

A Turberfield Scene script is a reStructuredText_ file.

The file name should contain lower case characters only, and have a suffix of
**.rst**.
It should contain no whitespace or punctuation characters. Underscores should
be used to represent spaces.

Structure
=========

#. The file should begin with a comment_ identifying it as a Turberfield
   scene script.
#. The file should contain metadata identifying the author(s) in a
   `field list`_. The following fields are recommended:

   * author
   * date
   * copyright

#. The file must contain at least one `entity declaration`_ before any
   scene is defined.
#. The file must contain at least one **scene** section which is created by a
   top-level heading_.
#. Each scene  must contain at least one **shot** section which is created by a
   second-level heading_.
#. Dialogue is defined by a citation_ reference in a shot section.
   The name given in the citation must match an entity declaration.
   Dialogue may contain `inline markup`_ and `substitution references`_.

Elements
========

Entity declaration
~~~~~~~~~~~~~~~~~~

.. rst:directive:: .. entity:: NAME

    The name of an entity should be in upper case.

    ``:roles:``
        A whitespace separated sequence of other entities.
        A match for this entity will be considered for those roles.
        Optional.
    ``:states:``
        A whitespace separated sequence of dotted paths.
        Each path must resolve to a Python Enum class.
        In addition, a single integer value is also allowed.
        A candidate for this entity must match *all* these state criteria.
        Optional.
    ``:types:``
        A whitespace separated sequence of dotted paths.
        Each path must resolve to a Python type.
        A candidate for this entity must be an instance of *at least one*
        of these types. Optional.


Turberfield uses several standard idioms from resTructuredText.

* Field tags for authorship
* Comments
* Top level title section denotes a Scene
* Second level title section denotes a Shot.
* Inline formatting for emphasis of dialogue
* Lines of dialogue attributed to entities via citation references
* Substitution definitions provide a way for one entity to refer
  to another in a line of dialogue.

* Folders contain sequences of action.
* Scripts separate action into scenes.
* Scenes are made up of shots.
* Shots can contain lines of dialogue or audio effects.

.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _field list: http://docutils.sourceforge.net/docs/user/rst/quickref.html#field-lists
.. _comment: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#comments
.. _inline markup: http://docutils.sourceforge.net/docs/user/rst/quickref.html#inline-markup
.. _heading: http://docutils.sourceforge.net/docs/user/rst/quickref.html#section-structure
.. _citation: http://docutils.sourceforge.net/docs/user/rst/quickref.html#citations
.. _substitution references: http://docutils.sourceforge.net/docs/user/rst/quickref.html#substitution-references-and-definitions
