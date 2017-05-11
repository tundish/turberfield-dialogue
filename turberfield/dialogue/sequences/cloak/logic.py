from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful
from turberfield.utils.assembly import Assembly


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

locations = {
    0: "Foyer",
    1: "Bar",
    2: "Cloakroom floor",
    3: "Cloakroom",
    4: "Cloakroom hook",
}

class Locatable(Stateful, Persona):
    pass

class Destructible(Stateful, Persona):
    pass

ensemble = [
    Locatable(name="Narrator"),
    Locatable(name="Cloak"),
    Destructible(name="Message"),
]

totality = ensemble

folder = SceneScript.Folder(
    "turberfield.dialogue.sequences.cloak",
    __doc__,
    ["foyer.rst", "bar.rst", "cloakroom.rst"],
    []
)
