from typing import Any
from game.characters.NonPlayableCharacter_ren import NonPlayableCharacter
from game.characters.character_traits_ren import CharacterTrait
from game.characters.npcs.chloe_ren import Chloe
from game.characters.npcs.chris_ren import Chris
from renpy.minstore import _

chloe = Chloe()
chris = Chris()

"""renpy
init python:
"""


class Nora(NonPlayableCharacter, object):
    def __init__(self) -> None:
        self.relationships = {}

        self.pending_text_messages = []
        self.text_messages = []

        self.pending_simplr_messages = []
        self.simplr_messages = []

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__()

        self.__dict__.update(state)

    @property
    def name(self) -> str:
        return _("Nora")

    @property
    def username(self) -> str:
        return _("Nora_12")

    @property
    def traits(self) -> CharacterTrait:
        return CharacterTrait.TALKATIVE

    @property
    def vindictive_characters(self) -> tuple[NonPlayableCharacter, ...]:
        return (chris, chloe)
