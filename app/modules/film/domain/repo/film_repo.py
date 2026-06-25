from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.modules.film.domain.film.entity import Film


class FilmRepoI(ABC):

    @abstractmethod
    def register_film(self,session: Session, film: Film) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_film_id(self, session: Session, film_id: int) -> None:
        raise NotImplementedError
