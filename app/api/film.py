from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db_session import get_session
from app.modules.film.application.use_case.register_films import register_films
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.modules.film.infrastructure.persistance.sql_repository.film_repo import SqlFilmRepo

router = APIRouter(prefix="")


@router.get("/store-films")
async def register_films_route(
    repo: FilmRepoI = Depends(SqlFilmRepo)
    ):
    all_films = []
    url = f"{settings.SWAPI_BASE_URL}/films/"

    async with httpx.AsyncClient() as client:
        while url:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            all_films.extend(data.get("results", []))
            url = data.get("next")

    registered = register_films(films=all_films, repo=repo)
    return {"registered": len(registered)}