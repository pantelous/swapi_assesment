from abc import ABC, abstractmethod

from app.modules.starship.domain.starship.entity import Starship


class StarshipRepoI(ABC):

    @abstractmethod
    def register_starship(self, starship: Starship) -> None:
        raise NotImplementedError

    @abstractmethod
    def link_starship_film(self, starship_id: int, film_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def link_starship_character(self, starship_id: int, character_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_starship_id(self, starship_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def search_starship(self, name: str) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_starships(self, limit: int, offset: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_films_for_starship(self, starship_id: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_pilots_for_starship(self, starship_id: int) -> list[dict]:
        raise NotImplementedError
