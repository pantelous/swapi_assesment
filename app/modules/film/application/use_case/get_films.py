from typing import Any

from pydantic import BaseModel, Field

from app.uow.swapi_uow import SwapiUoWI


class GetFilmsQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def get_films(
    uow: SwapiUoWI,
    query_params: GetFilmsQuery,
) -> list[dict[str, Any]]:

    with uow:
        films = uow.film_repo.get_films(
            limit=query_params.page_size,
            offset=query_params.offset,
        )

        result = []
        for film in films:
            characters = uow.film_repo.get_characters_for_film(film["id"])
            result.append({**film, "characters": characters})

        return result
