from PlayableCharacters_ren import PlayableCharacter

name: str

"""renpy
init python:
"""


class MainCharacter(PlayableCharacter):
    def __init__(self) -> None:
        self._username = name
        self._profile_picture = self.profile_pictures[0]

        self.relationships = {}
        self.inventory = []
