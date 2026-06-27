from typing import Any

from pydantic import BaseModel, model_validator

from app.uow.swapi_uow import SwapiUoWI


class SearchStarshipQuery(BaseModel):
    name: str

    @model_validator(mode='after')
    def name_not_empty(self) -> 'SearchStarshipQuery':
        if not self.name.strip():
            raise ValueError('Name cannot be empty')
        return self


def search_starships(
    uow: SwapiUoWI,
    query_params: SearchStarshipQuery,
) -> list[dict[str, Any]]:
    with uow:
        return uow.starship_repo.search_starship(name=query_params.name)
