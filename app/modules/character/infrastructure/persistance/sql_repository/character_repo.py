from typing import List

from sqlalchemy.orm import Session

from app.core.base_repository import SqlBaseRepository
from app.modules.character.domain.character.entity import Character
from app.modules.character.domain.repo.character_repo import CharacterRepoI
from app.core.sql_query import SqlQuery
from app.modules.character.infrastructure.persistance.sql_queries.character_query import (
    get_character_query,
    get_characters_paginated_query,
    get_films_for_character_query,
    insert_character_query,
    link_character_film_query,
    search_characters_by_name_query,
)

class SqlCharacterRepo(CharacterRepoI, SqlBaseRepository):

    def register_character(self, character: Character) -> Character:
        query, params = insert_character_query(character)
        sql_query = SqlQuery(self.session, query, params)
        sql_query.persist()
        return character

    def link_character_film(self, swapi_character_id: int, swapi_film_id: int) -> None:
        query, params = link_character_film_query(swapi_character_id, swapi_film_id)
        SqlQuery(self.session, query, params).persist()

    def load_character_id(self, character_id: int) -> None:
        query, params = get_character_query(character_id)
        sql_query = SqlQuery(self.session, query, params)
        return sql_query.fetch_one()
    
    def search_character(self, character_name: int) -> None:
        query, params = search_characters_by_name_query(character_name)
        sql_query = SqlQuery(self.session, query, params)
        return sql_query.fetch_all()

    def get_characters(self, limit: int, offset: int) -> list[dict]:
        query, params = get_characters_paginated_query(limit, offset)
        sql_query = SqlQuery(self.session, query, params)
        return sql_query.fetch_all()

    def get_films_for_character(self, character_id: int) -> list[dict]:
        query, params = get_films_for_character_query(character_id)
        sql_query = SqlQuery(self.session, query, params)
        return sql_query.fetch_all()
        