import itertools

from turberfield.dialogue.model import SceneScript

__doc__ = """
A simple drama for demonstration.

"""

folder = SceneScript.Folder(
    "turberfield.dialogue.sequences.battle_royal",
    __doc__, None,
    ["combat.rst"], itertools.repeat(None)
)
