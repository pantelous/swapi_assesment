from typing import Any

from pydantic import BaseModel, model_validator

from app.uow.swapi_uow import SqlSwapiUoW


class SearchFilmQuery(BaseModel):
    title: str

    @model_validator(mode='after')
    def title_not_empty(self) -> 'SearchFilmQuery':
        if not self.title.strip():
            raise ValueError('Title cannot be empty')
        return self


def search_films(
    uow: SqlSwapiUoW,
    query_params: SearchFilmQuery,
) -> list[dict[str, Any]]:
    with uow:
        return uow.film_repo.search_film(title=query_params.title)
