from typing import Any

from pydantic import BaseModel, model_validator
from sqlalchemy.orm import Session

from app.core.sql_query import SqlQuery
from app.modules.character.infrastructure.persistance.sql_queries.character_query import search_characters_by_name_query
from app.uow.swapi_uow import SqlSwapiUoW


class SearchCharacterQuery(BaseModel):
    name: str

    @model_validator(mode='after')
    def name_not_empty(self) -> 'SearchCharacterQuery':
        if not self.name.strip():
            raise ValueError('Name cannot be empty')
        return self


def search_characters(
    uow: SqlSwapiUoW,
    query_params: SearchCharacterQuery
) -> list[dict[str, Any]]:

    with uow:
        character_name = uow.character_repo.search_character(character_name=query_params.name)
        return character_name
