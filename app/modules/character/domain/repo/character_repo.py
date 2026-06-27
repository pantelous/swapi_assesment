from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session

from app.modules.character.domain.character.entity import Character


class CharacterRepoI(ABC):

    @abstractmethod
    def register_character(self, character: Character) -> None:
        raise NotImplementedError

    @abstractmethod
    def link_character_film(self, swapi_character_id: int, swapi_film_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def load_character_id(self, character_id: int) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def search_character(self, character_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_characters(self, limit: int, offset: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_films_for_character(self, character_id: int) -> list[dict]:
        raise NotImplementedError