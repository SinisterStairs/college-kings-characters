from game.characters.character_traits_ren import CharacterTrait
from renpy.minstore import _

from game.characters.NonPlayableCharacter_ren import NonPlayableCharacter

nora: NonPlayableCharacter

"""renpy
init python:
"""


class Chloe(NonPlayableCharacter, object):
    def __init__(self) -> None:
        self.points = 0

        self.relationships = {}

        self.pending_text_messages = []
        self.text_messages = []

        self.pending_simplr_messages = []
        self.simplr_messages = []

    @property
    def name(self) -> str:
        return _("Chloe")

    @property
    def username(self) -> str:
        return _("Chloe101")

    @property
    def traits(self) -> CharacterTrait:
        return CharacterTrait.COMPETITIVE

    @property
    def vindictive_characters(self) -> tuple[NonPlayableCharacter, ...]:
        return (nora,)
