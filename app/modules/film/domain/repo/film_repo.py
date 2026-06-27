from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.modules.film.domain.film.entity import Film


class FilmRepoI(ABC):

    @abstractmethod
    def register_film(self, film: Film) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_film_id(self, film_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def search_film(self, title: str) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def get_films(self, limit: int, offset: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_characters_for_film(self, film_id: int) -> list[dict]:
        raise NotImplementedError
