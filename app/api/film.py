from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.injections.get_swapi_uow import get_swapi_uow
from app.core.config import settings
from app.modules.film.application.use_case.get_films import GetFilmsQuery, get_films
from app.modules.film.application.use_case.register_films import register_films
from app.modules.film.application.use_case.search_films import SearchFilmQuery, search_films
from app.uow.swapi_uow import SqlSwapiUoW

router = APIRouter(prefix="")


@router.get("/store-films", summary = "Store films from SWAPI")
async def register_films_route(
    uow: SqlSwapiUoW = Depends(get_swapi_uow)
    ):
    all_films = []
    url = f"{settings.SWAPI_BASE_URL}/films/"

    async with httpx.AsyncClient() as client:
        try:
            while url:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                all_films.extend(data.get("results", []))
                url = data.get("next")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="API request timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"API returned {e.response.status_code}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail="Could not reach API")
    registered = register_films(films=all_films, uow=uow)
    return {"registered": len(registered)}

@router.get("/get-films", summary="Get all films from the database")
def get_films_route(
    query_params: Annotated[GetFilmsQuery, Query()],
    uow: SqlSwapiUoW = Depends(get_swapi_uow),
):
    return get_films(uow=uow, query_params=query_params)


@router.get("/search-film", summary="Search films from db")
def film_search_route(
    query_params: Annotated[SearchFilmQuery, Query()],
    uow: SqlSwapiUoW = Depends(get_swapi_uow),
):
    return search_films(uow=uow, query_params=query_params)


@router.get("/fetch-films", summary = "Just Fetch and display films from SWAPI")
async def fectch_films_route():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.SWAPI_BASE_URL}/films/")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Films not found")
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="API request timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"API returned {e.response.status_code}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail="Could not reach API")
