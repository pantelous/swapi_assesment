from typing import Any

from pydantic import BaseModel, Field

from app.uow.swapi_uow import SwapiUoWI


class GetCharactersQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


def get_characters(
    uow: SwapiUoWI,
    query_params: GetCharactersQuery,
) -> list[dict[str, Any]]:

    with uow:
        characters = uow.character_repo.get_characters(
            limit=query_params.page_size,
            offset=query_params.offset,
        )

        result = []
        for character in characters:
            films = uow.character_repo.get_films_for_character(character["id"])
            result.append({**character, "films": films})

        return result
