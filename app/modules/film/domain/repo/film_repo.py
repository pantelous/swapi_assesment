from abc import ABC, abstractmethod
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
    def get_film_by_name(self, film_name: str) -> Film:
        raise NotImplementedError

    @abstractmethod
    def get_characters_for_film(self, film_id: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def link_film_starship(self, film_id: int, starship_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update_film_votes(self, film: Film) -> Film:
        raise NotImplementedError
