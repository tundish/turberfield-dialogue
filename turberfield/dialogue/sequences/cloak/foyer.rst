..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

:author: D Haynes
:date: 2017-05-11

.. entity:: NARRATOR
   :states: 0

.. entity:: CLOAK
   :states: 0


The Foyer of an abandoned Hotel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Looking around
--------------

[NARRATOR]_

    It appears this building used to be a Hotel.

Checking my person
------------------

[CLOAK]_

    You are wearing a long cloak, which gathers around you. It feels furry,
    like velvet, although that's hard to tell by looking. It is so black
    that its folds and textures cannot be perceived. It seems to swallow all
    light.

.. memory:: turberfield.dialogue.sequences.cloak.logic.Progress.described
   :subject: NARRATOR
   :object: CLOAK

   |Narrator| described the |Cloak|.

.. |Narrator| property:: Narrator.name.firstname
.. |Cloak| property:: Cloak.name.firstname
