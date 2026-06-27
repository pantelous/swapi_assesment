from __future__ import annotations
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session, sessionmaker

from app.core.base_uow import BaseUoW
from app.core.db import LazySessionLocal
from app.modules.character.domain.repo.character_repo import CharacterRepoI
from app.modules.character.infrastructure.persistance.sql_repository.character_repo import SqlCharacterRepo
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.modules.film.infrastructure.persistance.sql_repository.film_repo import SqlFilmRepo

class SwapiUoWI(ABC):
    character_repo: CharacterRepoI
    film_repo: FilmRepoI

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
    

    def __enter__(self):
        self.session: Session = self.session_factory().__enter__()
        self.character_repo = SqlCharacterRepo(self.session)
        self.film_repo = SqlFilmRepo(self.session)
        return self
