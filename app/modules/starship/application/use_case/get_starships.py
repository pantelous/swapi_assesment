from typing import Any

from pydantic import BaseModel, Field

from app.uow.swapi_uow import SwapiUoWI


class GetStarshipsQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def get_starships(
    uow: SwapiUoWI,
    query_params: GetStarshipsQuery,
) -> list[dict[str, Any]]:

    with uow:
        starships = uow.starship_repo.get_starships(
            limit=query_params.page_size,
            offset=query_params.offset,
        )

        result = []
        for starship in starships:
            films = uow.starship_repo.get_films_for_starship(starship["id"])
            pilots = uow.starship_repo.get_pilots_for_starship(starship["id"])
            result.append({**starship, "films": films, "pilots": pilots})

        return result
