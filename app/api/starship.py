from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.injections.get_swapi_uow import get_swapi_uow
from app.core.config import settings
from app.modules.starship.application.use_case.get_starships import GetStarshipsQuery, get_starships
from app.modules.starship.application.use_case.register_starships import register_starships
from app.modules.starship.application.use_case.search_starships import SearchStarshipQuery, search_starships
from app.uow.swapi_uow import SqlSwapiUoW

router = APIRouter(prefix="")

@router.get("/store-starships")
async def register_starships_route(
    uow: SqlSwapiUoW = Depends(get_swapi_uow),
):
    all_starships = []
    url = f"{settings.SWAPI_BASE_URL}/starships/"

    async with httpx.AsyncClient() as client:
        try:
            while url:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                all_starships.extend(data.get("results", []))
                url = data.get("next")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="API request timed out")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"API returned {e.response.status_code}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail="Could not reach API")

    registered = register_starships(starships=all_starships, uow=uow)
    return {"registered": len(registered)}


@router.get("/get-starships")
def get_starships_route(
    query_params: Annotated[GetStarshipsQuery, Query()],
    uow: SqlSwapiUoW = Depends(get_swapi_uow),
):
    return get_starships(uow=uow, query_params=query_params)


@router.get("/search-starship")
def search_starship_route(
    query_params: Annotated[SearchStarshipQuery, Query()],
    uow: SqlSwapiUoW = Depends(get_swapi_uow),
):
    return search_starships(uow=uow, query_params=query_params)


@router.get("/fetch-starships")
async def fetch_starships_route():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{settings.SWAPI_BASE_URL}/starships/")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Starships not found")
            response.raise_for_status()
            return response.json()
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="SWAPI request timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"SWAPI returned {e.response.status_code}")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Could not reach SWAPI")
