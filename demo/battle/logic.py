from itertools import repeat

from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Persona
from turberfield.dialogue.types import Stateful


class Animal(Stateful, Persona):
    pass

class Tool(Stateful, Persona):
    pass

references = [
    Animal(name="Itchy").set_state(1),
    Animal(name="Scratchy").set_state(1),
    Tool(name="Ol' Rusty Chopper").set_state(1),
]

folder = SceneScript.Folder(
    pkg=__name__,
    description="Cartoon battle demo",
    metadata=None,
    paths=["combat.rst"],
    interludes=repeat(None)
)
