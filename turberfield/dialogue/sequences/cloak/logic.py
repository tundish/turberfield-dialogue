import enum
from itertools import repeat

from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful


__doc__ = """
From http://www.firthworks.com/roger/cloak/::

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

"""

@enum.unique
class Location(EnumFactory, enum.Enum):
    foyer = 0
    bar = 1
    cloakroom_floor = 2
    cloakroom = 3
    cloakroom_hook = 4

@enum.unique
class Progress(EnumFactory, enum.Enum):
    destroyed = 0
    described = 1
    read = 2

class Narrator(Stateful, Persona):
    pass

class Garment(Stateful, Persona):
    pass

class Prize(Stateful, Persona):
    pass


ensemble = [
    Narrator(name="").set_state(Location.foyer),
    Garment(name="Cloak").set_state(Location.foyer),
    Prize(name="Message")
]


def parse_command(cmd):
    try:
        return cmd.strip().split(" ")[-1][0].lower()
    except:
        return None


def interaction(folder, ensemble, log=None, loop=None):
    narrator = next(i for i in ensemble if isinstance(i, Narrator))
    cloak = next(i for i in ensemble if isinstance(i, Garment))
    locn = narrator.get_state(Location)
    action = None
    if locn == Location.foyer:
        while action not in ("s", "w"):
            cmd = input("Enter a command: ")
            action = parse_command(cmd)
        if action == "s":
            narrator.set_state(Location.bar)
        else:
            narrator.set_state(Location.cloakroom)
        if cloak.get_state(Location) == locn:
            cloak.set_state(narrator.get_state(Location))
    else:
        print(narrator)
    return folder

references = ensemble + [Location, Progress]

game = SceneScript.Folder(
    "turberfield.dialogue.sequences.cloak",
    __doc__, None,
    ["foyer.rst", ],
    #["foyer.rst", "bar.rst", "cloakroom.rst"],
    repeat(interaction)
)
