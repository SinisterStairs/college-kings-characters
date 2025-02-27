from typing import Any, Iterable, Optional, Union

from game.characters.npcs.svc_housing_officer_ren import SVCHousingOfficer
from renpy import store
import renpy.exports as renpy

from game.characters.base_character_ren import BaseCharacter
from game.characters.NonPlayableCharacter_ren import NonPlayableCharacter
from game.characters.main_character_ren import MainCharacter
from game.characters.Relationship_ren import Relationship
from game.characters.Moods_ren import Moods
from game.characters.PlayableCharacters_ren import PlayableCharacter

mc: MainCharacter
"""renpy
init python:
"""


class CharacterService:
    @staticmethod
    def get_user_by_str(name: str) -> BaseCharacter:
        name = name.lower()
        try:
            return getattr(store, name.replace(" ", "_"))
        except AttributeError:
            try:
                if name == "svc housing officer":
                    return SVCHousingOfficer()
                return getattr(store, name.title().replace(" ", ""))()
            except AttributeError:
                raise AttributeError(f"{name} is not a valid character.")

    @staticmethod
    def get_user(character: Union[BaseCharacter, str]) -> BaseCharacter:
        if isinstance(character, str):
            return CharacterService.get_user_by_str(character)

        try:
            if isinstance(character, PlayableCharacter):
                return mc
            else:
                return getattr(store, character.name.lower().replace(" ", "_"))
        except AttributeError:
            raise AttributeError(f"{character} is not a valid character.")

    @staticmethod
    def get_relationship(
        character: BaseCharacter, target: Optional[BaseCharacter] = None
    ) -> "Relationship":
        if target is None:
            target = mc

        if not hasattr(character, "relationships"):
            character.relationships = {}

        if isinstance(target.relationships, set):
            target.relationships = {r: Relationship.FWB for r in target.relationships}

        if isinstance(character.relationships, set):
            character.relationships = {
                r: Relationship.FWB for r in character.relationships
            }

        if (
            target.relationships.get(character, Relationship.STRANGER).value
            > character.relationships.get(target, Relationship.STRANGER).value
        ):
            character.relationships[target] = target.relationships[character]

        return character.relationships.setdefault(target, Relationship.FRIEND)

    @staticmethod
    def compat_get_max_rel(
        npc_vars: dict[str, Any], target_vars: dict[str, Any]
    ) -> "Relationship":
        current_rel = Relationship.FRIEND

        mc_rels = target_vars.get("relationships", {})
        npc_name = npc_vars["name"]

        # region MC
        mc_rel = mc_rels.get(npc_name, Relationship.FRIEND)
        if mc_rel.value > current_rel.value:
            current_rel = mc_rel
        # endregion

        # region _relationship
        npc_rel = npc_vars.get("_relationship", Relationship.FRIEND)
        if npc_rel.value > current_rel.value:
            current_rel = npc_rel
        # endregion

        # region relationships
        npc_rel = npc_vars.get("relationship", Relationship.FRIEND)
        if npc_rel.value > current_rel.value:
            current_rel = npc_rel
        # endregion

        return current_rel

    @staticmethod
    def has_relationship(
        character: BaseCharacter,
        relationship: "Relationship",
        target: Optional[BaseCharacter] = None,
    ) -> bool:
        if target is None:
            target = mc

        return CharacterService.get_relationship(character, target) == relationship

    @staticmethod
    def set_relationship(
        character: BaseCharacter,
        relationship: "Relationship",
        target: Optional[BaseCharacter] = None,
    ) -> None:
        if target is None:
            target = mc

        if not hasattr(character, "relationships"):
            character.relationships = {}

        if not hasattr(target, "relationships"):
            target.relationships = {}

        if isinstance(target.relationships, set):
            target.relationships = {r: Relationship.FWB for r in target.relationships}

        character.relationships[target] = relationship
        target.relationships[character] = relationship

    @staticmethod
    def get_mood(character: "NonPlayableCharacter") -> "Moods":
        try:
            return character.mood
        except AttributeError:
            character.mood = Moods.NORMAL

        return character.mood

    @staticmethod
    def has_mood(character: "NonPlayableCharacter", mood: "Moods") -> bool:
        try:
            character.mood
        except AttributeError:
            character.mood = Moods.NORMAL

        return mood == character.mood or character.mood & mood == mood

    @staticmethod
    def set_mood(character: "NonPlayableCharacter", mood: "Moods") -> None:
        character.mood = mood

    @staticmethod
    def reset_mood(character: "NonPlayableCharacter") -> None:
        character.mood = Moods.NORMAL

    @staticmethod
    def add_mood(character: "NonPlayableCharacter", mood: "Moods") -> None:
        if character.mood == Moods.NORMAL:
            character.mood = mood
            return

        character.mood |= mood

    @staticmethod
    def remove_mood(character: "NonPlayableCharacter", mood: "Moods") -> None:
        character.mood &= ~mood

    @staticmethod
    def get_profile_pictures(character_name: str) -> tuple[str, ...]:
        directory: str = f"characters/images/{character_name.lower()}"

        try:
            return tuple(
                file for file in renpy.list_files() if file.startswith(directory)
            )
        except OSError:
            return tuple(
                file
                for file in renpy.list_files()
                if file.startswith("characters/images/chloe")
            )

    @staticmethod
    def is_exclusive_girlfriend(
        character: BaseCharacter, target: Optional[BaseCharacter] = None
    ) -> bool:
        if target is None:
            target = mc

        return any(
            CharacterService.is_girlfriend(npc)
            for npc in target.relationships
            if npc != character
        )

    @staticmethod
    def is_girlfriend(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(
            character, Relationship.GIRLFRIEND, target
        )

    @staticmethod
    def is_girlfriends(
        characters: Iterable[BaseCharacter],
        target: Optional[BaseCharacter] = None,
    ) -> bool:
        if target is None:
            target = mc

        return all(
            CharacterService.is_girlfriend(character, target)
            for character in characters
        )

    @staticmethod
    def is_exclusive(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return any(
            CharacterService.is_girlfriend(npc) or CharacterService.is_fwb(npc)
            for npc in target.relationships
            if npc != character
        )

    @staticmethod
    def is_fwb(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.FWB, target)

    @staticmethod
    def is_fwbs(
        characters: Iterable[BaseCharacter],
        target: Optional[BaseCharacter] = None,
    ) -> bool:
        if target is None:
            target = mc

        return all(
            CharacterService.is_fwb(character, target) for character in characters
        )

    @staticmethod
    def is_dating(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.DATING, target)

    @staticmethod
    def is_kissed(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.KISSED, target)

    @staticmethod
    def is_friend(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.FRIEND, target)

    @staticmethod
    def is_friends(
        characters: Iterable[BaseCharacter],
        target: Optional[BaseCharacter] = None,
    ) -> bool:
        if target is None:
            target = mc

        return all(
            CharacterService.is_friend(character, target) for character in characters
        )

    @staticmethod
    def is_ex(character: BaseCharacter, target: Optional[BaseCharacter] = None) -> bool:
        if target is None:
            target = mc

        return CharacterService.has_relationship(character, Relationship.EX, target)

    @staticmethod
    def is_exes(
        characters: Iterable[BaseCharacter],
        target: Optional[BaseCharacter] = None,
    ):
        if target is None:
            target = mc

        return all(
            CharacterService.is_ex(character, target) for character in characters
        )

    @staticmethod
    def is_mad(character: "NonPlayableCharacter") -> bool:
        return CharacterService.has_mood(character, Moods.MAD)

    @staticmethod
    def is_threatened(character: "NonPlayableCharacter") -> bool:
        return CharacterService.has_mood(character, Moods.THREATENED)
