from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.injections.get_swapi_uow import get_swapi_uow
from app.core.config import settings
from app.uow.swapi_uow import SqlSwapiUoW
from app.modules.character.application.use_case.register_characters import register_characters
from app.modules.character.application.use_case.get_characters import GetCharactersQuery, get_characters
from app.modules.character.application.use_case.search_characters import SearchCharacterQuery, search_characters
from app.modules.character.domain.repo.character_repo import CharacterRepoI
from app.modules.character.infrastructure.persistance.sql_repository.character_repo import SqlCharacterRepo

router = APIRouter(prefix="")


@router.get("/store-characters")
async def register_characters_route(
    uow: SqlSwapiUoW = Depends(get_swapi_uow)
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

    registered = register_characters(characters=all_characters, uow= uow)
    return {"registered": len(registered)}


@router.get("/get-characters")
def get_characters_route(
    query_params: Annotated[GetCharactersQuery, Query()],
    uow: SqlSwapiUoW = Depends(get_swapi_uow),
):
    return get_characters(uow=uow, query_params=query_params)


@router.get("/search-character")
def character_search_route(
    query_params: Annotated[SearchCharacterQuery, Query()],
    uow: SqlSwapiUoW = Depends(get_swapi_uow)
):
    return search_characters(uow=uow, query_params=query_params)


@router.get("/fetch-characters")
async def fectch_characters_route():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.SWAPI_BASE_URL}/people/")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Characters not found")
        response.raise_for_status()
        return response.json()
