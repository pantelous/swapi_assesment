from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db_session import get_session
from app.modules.character.application.use_case.register_characters import register_characters
from app.modules.character.application.use_case.search_characters import SearchCharacterQuery, search_characters
from app.modules.character.domain.repo.character_repo import CharacterRepoI
from app.modules.character.infrastructure.persistance.sql_repository.character_repo import SqlCharacterRepo

router = APIRouter(prefix="")


@router.get("/store-characters")
async def register_characters_route(
    repo: CharacterRepoI = Depends(SqlCharacterRepo)
    ):
    all_characters = []
    url = f"{settings.SWAPI_BASE_URL}/people/"

    async with httpx.AsyncClient() as client:
        while url:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            all_characters.extend(data.get("results", []))
            url = data.get("next")

    registered = register_characters(characters=all_characters, repo=repo)
    return {"registered": len(registered)}


@router.get("/search-character")
def character_search_route(
    query_params: Annotated[SearchCharacterQuery, Query()],
    session: Session = Depends(get_session),
):
    return search_characters(session=session, query_params=query_params)


@router.get("/{character_id}")
async def get_character_route(character_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.SWAPI_BASE_URL}/people/{character_id}/")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Character not found")
        response.raise_for_status()
        return response.json()
