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

.. property:: FIGHTER_1.state turberfield.dialogue.sequences.battle_royal.types.Animation.angry
.. property:: FIGHTER_2.state turberfield.dialogue.sequences.battle_royal.types.Animation.passive

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

.. property:: FIGHTER_2.state turberfield.dialogue.sequences.battle_royal.types.Animation.dying
.. property:: FIGHTER_2.state 0

.. memory:: turberfield.dialogue.sequences.battle_royal.types.Pose.toppled
   :subject: FIGHTER_1
   :object: FIGHTER_2

   |Fighter1| cruelly defeated |Fighter2| in a brutal surprise attack.

 
.. |Fighter1| property:: FIGHTER_1.name.firstname
.. |Fighter2| property:: FIGHTER_2.name.firstname
