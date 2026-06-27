from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.injections.get_swapi_uow import get_swapi_uow
from app.core.config import settings
from app.modules.film.application.use_case.register_films import register_films
from app.modules.film.application.use_case.search_films import SearchFilmQuery, search_films
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.modules.film.infrastructure.persistance.sql_repository.film_repo import SqlFilmRepo
from app.uow.swapi_uow import SqlSwapiUoW

router = APIRouter(prefix="")


@router.get("/fetch-starships")
async def fectch_starships_route():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.SWAPI_BASE_URL}/starships/")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="starships not found")
        response.raise_for_status()
        return response.json()