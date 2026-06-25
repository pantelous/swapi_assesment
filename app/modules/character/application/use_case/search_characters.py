from typing import Any

from pydantic import BaseModel, model_validator
from sqlalchemy.orm import Session

from app.core.sql_query import SqlQuery
from app.modules.character.infrastructure.persistance.sql_queries.character_query import search_characters_by_name_query


class SearchCharacterQuery(BaseModel):
    name: str

    @model_validator(mode='after')
    def name_not_empty(self) -> 'SearchCharacterQuery':
        if not self.name.strip():
            raise ValueError('Name cannot be empty')
        return self


def search_characters(
    session: Session,
    query_params: SearchCharacterQuery,
) -> list[dict[str, Any]]:

    with session:
        query, params = search_characters_by_name_query(query_params.name)
        sql_query = SqlQuery(session, query, params)
        return sql_query.fetch_all()
