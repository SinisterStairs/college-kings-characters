from renpy.minstore import _

from game.characters.NonPlayableCharacter_ren import NonPlayableCharacter

"""renpy
init python:
"""


class SVCHousingOfficer(NonPlayableCharacter, object):
    def __init__(self) -> None:
        self.relationships = {}

        self.pending_text_messages = []
        self.text_messages = []

        self.pending_simplr_messages = []
        self.simplr_messages = []

        self.points = 0

    @property
    def name(self) -> str:
        return _("SVC Housing Officer")

    @property
    def username(self) -> str:
        return _("SVC Housing Officer")
