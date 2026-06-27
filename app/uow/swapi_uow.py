from __future__ import annotations
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session, sessionmaker

from app.core.base_uow import BaseUoW
from app.core.db import LazySessionLocal
from app.modules.character.domain.repo.character_repo import CharacterRepoI
from app.modules.character.infrastructure.persistance.sql_repository.character_repo import SqlCharacterRepo
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.modules.film.infrastructure.persistance.sql_repository.film_repo import SqlFilmRepo
from app.modules.starship.domain.repo.starship_repo import StarshipRepoI
from app.modules.starship.infrastructure.persistance.sql_repository.starship_repo import SqlStarshipRepo

class SwapiUoWI(ABC):
    character_repo: CharacterRepoI
    film_repo: FilmRepoI
    starship_repo: StarshipRepoI

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, *args) -> None:
        raise NotImplementedError

    def __return__(self) -> SwapiUoWI:
        return self

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class SqlSwapiUoW(BaseUoW, SwapiUoWI):
    session: Session
    session_factory: LazySessionLocal
    film_repo: FilmRepoI
    character_repo: CharacterRepoI
    starship_repo: StarshipRepoI

    def __enter__(self):
        self.session: Session = self._open_session()
        self.character_repo = SqlCharacterRepo(self.session)
        self.film_repo = SqlFilmRepo(self.session)
        self.starship_repo = SqlStarshipRepo(self.session)
        return self

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.session.close()