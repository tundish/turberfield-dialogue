..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

:author: D Haynes
:date: 2016-10-15

.. entity:: FIGHTER_1

.. entity:: FIGHTER_2
   :types: turberfield.dialogue.sequences.battle_royal.types.Animal

.. entity:: WEAPON
   :types: turberfield.dialogue.sequences.battle_royal.types.Furniture
           turberfield.dialogue.sequences.battle_royal.types.Tool


Combat
~~~~~~


Action
------

.. property:: FIGHTER_1.animation turberfield.dialogue.sequences.battle_royal.types.Animation.angry
.. property:: FIGHTER_2.animation turberfield.dialogue.sequences.battle_royal.types.Animation.passive

[FIGHTER_1]_


    I hate the way you use me, |Fighter2| !

[WEAPON]_

    **Whack!**

[FIGHTER_2]_

    Uuurrggh!

.. property:: FIGHTER_2.state turberfield.dialogue.sequences.battle_royal.types.Animation.dying

.. |Fighter2| property:: FIGHTER_2.name
