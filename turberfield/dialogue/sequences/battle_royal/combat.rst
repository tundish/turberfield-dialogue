..  This is a Turberfield dialogue file (reStructuredText).
    Scene ~~
    Shot --

:author: D Haynes
:date: 2016-10-15

.. entity:: FIGHTER_1
   :states: 1
   :roles: WEAPON

.. entity:: FIGHTER_2
   :types: turberfield.dialogue.sequences.battle_royal.types.Animal
   :states: 1

.. entity:: WEAPON
   :types: turberfield.dialogue.sequences.battle_royal.types.Tool


Combat
~~~~~~


Action
------

[FIGHTER_1]_

    I hate the way you use me, |Fighter2| !

.. fx:: turberfield.dialogue.sequences.battle_royal slapwhack.wav
   :offset: 0
   :duration: 3000
   :loop: 1

[WEAPON]_

    **Whack!**

[FIGHTER_2]_

    Uuurrggh!

.. property:: FIGHTER_2.state 0

.. |Fighter1| property:: FIGHTER_1.name.firstname
.. |Fighter2| property:: FIGHTER_2.name.firstname
