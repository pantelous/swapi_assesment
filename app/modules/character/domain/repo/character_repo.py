from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session

from app.modules.character.domain.character.entity import Character


class CharacterRepoI(ABC):

    @abstractmethod
    def register_character(self, session: Session, character: Character) -> None:
        raise NotImplementedError

    @abstractmethod
    def link_character_film(self, session: Session, swapi_character_id: int, swapi_film_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def load_character_id(self, session: Session, character_id: int) -> None:
        raise NotImplementedError