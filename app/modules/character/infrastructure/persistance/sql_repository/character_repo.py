from typing import List

from sqlalchemy.orm import Session

from app.modules.character.domain.character.entity import Character
from app.modules.character.domain.repo.character_repo import CharacterRepoI
from app.core.sql_query import SqlQuery
from app.modules.character.infrastructure.persistance.sql_queries.character_query import (
    get_character_query,
    insert_character_query,
    link_character_film_query,
)
from app.modules.character.infrastructure.transformers.character_transformers import transform_character_data


class SqlCharacterRepo(CharacterRepoI):

    def register_character(self,session: Session, character: Character) -> Character:
        query, params = insert_character_query(character)
        sql_query = SqlQuery(session, query, params)
        sql_query.persist()
        return character

    def link_character_film(self, session: Session, swapi_character_id: int, swapi_film_id: int) -> None:
        query, params = link_character_film_query(swapi_character_id, swapi_film_id)
        SqlQuery(session, query, params).persist()

    def load_character_id(self,session: Session, character_id: int) -> None:
        query, params = get_character_query(character_id)
        sql_query = SqlQuery(session, query, params)
        return sql_query.fetch_one()
        