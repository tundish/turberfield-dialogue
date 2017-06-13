..  Titling
    ##++::==~~--''``

Example 2: Cloak of Darkness
::::::::::::::::::::::::::::

Relate as an exploration.


* integer state used for masked/unmasked
* no :roles: hence some parts unvoiced
* infinite repeat
* interlude - what depth of detail?

Turberfield-dialogue is a screenplay system; it's not intended by itself to be
a game framework.

Nonetheless, it seems to me that it should be able to support you in *prototyping*
your game if the narrative is driven by dialogue.

So I decided to implement Cloak of Darkness to prove it could be done.
Cloak of Darkness is hello world.

.. admonition:: CoD?

    From http://www.firthworks.com/roger/cloak/:

    The Foyer of the Opera House is where the game begins. This empty room
    has doors to the south and west, also an unusable exit to the north.
    There is nobody else around.

    The Bar lies south of the Foyer, and is initially unlit. Trying to do
    anything other than return northwards results in a warning message about
    disturbing things in the dark.

    On the wall of the Cloakroom, to the west of the Foyer, is fixed a small
    brass hook.

    Taking an inventory of possessions reveals that the player is wearing a
    black velvet cloak which, upon examination, is found to be light-absorbent.

    The player can drop the cloak on the floor of the Cloakroom or better, put
    it on the hook.

    Returning to the Bar without the cloak reveals that the room is now lit.
    A message is scratched in the sawdust on the floor.

    The message reads either "You have won" or "You have lost", depending on
    how much it was disturbed by the player while the room was dark.

    The act of reading the message ends the game.

Interludes
==========

When you declare a folder object with scene script files, there's also an opportunity
for interludes. The fifth argument to :py:class:`~turberfield.dialogue.model.SceneScript.Folder`
is a sequence of functions. We ignored that opportunity in Battle; itertools.repeat(None).

An interlude is a function which gets called at the end of a scene file. The function
gets access to the folder you're using. It knows which of the scenes has just finished.
It also gets to see all the references you passed in to the performance. An interlude
function's return value is always a folder object; either the same folder (continue)
or another one (change the narrative for another).

So you can use the interlude to branch your story, even to add or remove personae from
references.

Masking
=======

In the previous example we used an integer state variable to mark the fighters as alive or
dead. This time, we'll reuse that concept. As the player moves around, certain objects
become active, or go quiet.

We'll need two other states; location of the player and the level of damage to the message.
Logic.py
========

* Adding a Location; explain enum
* Types; Narrator, Cloak, Prize are not *Personae*
* Integer state masks activity

The top of a Python module is where imports go:

.. code-block:: python

    import enum
    from itertools import repeat
    import random

    from turberfield.dialogue.model import SceneScript
    from turberfield.dialogue.types import EnumFactory
    from turberfield.dialogue.types import DataObject
    from turberfield.dialogue.types import Stateful

Next we declare an enumeration state which will define the
location of the player:

.. code-block:: python

    @enum.unique
    class Location(EnumFactory, enum.Enum):
        foyer = 0
        bar = 1
        cloakroom_floor = 2
        cloakroom = 3
        cloakroom_hook = 4

There are no Persona in this game; none of the voices has a name.
But they do have state, and some of them need attributes. The
useful types to inherit from will be *Stateful* and *DataObject*.

Each of the entities in the game gets its own class declaration:

.. code-block:: python

    class Narrator(Stateful):
        pass

    class Cloak(Stateful, DataObject):
        pass

    class Prize(Stateful, DataObject):
        pass

So now we can declare an ensemble of entities, setting attributes
and initial state where appropriate:

.. code-block:: python

    ensemble = [
        Narrator().set_state(Location.foyer),
        Cloak().set_state(Location.foyer).set_state(1),
        Prize(message="You win!")
    ]


This is an interactive game. We will be taking user input and
trying to act on commands if we see them. Here is the world's
dumbest text parser:

.. code-block:: python

    def parse_command(cmd):
        try:
            return cmd.strip().split(" ")[-1][0].lower()
        except:
            return None


::

    def interaction(folder, index, ensemble, cmd="", log=None, loop=None):
        narrator, cloak, prize, *others = ensemble
        locn = narrator.get_state(Location)
        action = None
        if locn == Location.foyer:
            while action not in ("s", "w", "q"):
                action = parse_command(cmd or input("Enter a command: "))
            if action == "s":
                narrator.set_state(Location.bar)
                if cloak.get_state(Location) == locn:
                    prize.set_state(0)
                else:
                    prize.set_state(1)
            elif action == "w":
                narrator.set_state(Location.cloakroom)
                cloak.set_state(1)
            else:
                return None
        elif locn == Location.bar:
            while action != "n":
                action = parse_command(cmd or input("Enter a command: "))

            narrator.set_state(Location.foyer)
            prize.message = prize.message.replace(
                random.choice(prize.message), " ", 1
            )
            prize.set_state(0)
        elif locn == Location.cloakroom:
            while action not in ("c", "h", "e"):
                action = parse_command(cmd or input("Enter a command: "))
            if action == "c":
                if cloak.get_state(Location) == Location.cloakroom:
                    cloak.set_state(Location.cloakroom_floor)
                else:
                    cloak.set_state(Location.cloakroom)
            elif action == "h":
                cloak.set_state(Location.cloakroom_hook)
            else:
                narrator.set_state(Location.foyer)
                if cloak.get_state(Location) != locn:
                    cloak.set_state(0)

        if cloak.get_state(Location) == locn:
            cloak.set_state(narrator.get_state(Location))
            cloak.set_state(1)

        return folder

    references = ensemble + [Location]

    folder = SceneScript.Folder(
        pkg=__name__,
        description="The 'Hello World' of text games.",
        metadata=None,
        paths=["foyer.rst", "bar.rst", "cloakroom.rst"],
        interludes=repeat(interaction)
    )

Memory
======

::

    "select s.name, state.name, o.name, note.text "
    "from state join touch on state.id = touch.state "
    "join entity as s on touch.sbjct = s.id "
    "left outer join entity as o on touch.objct = o.id "
    "left outer join note on note.touch = touch.id"

