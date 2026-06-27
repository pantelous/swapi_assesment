from typing import Any, List

from app.modules.character.application.use_case.register_characters import id_from_url
from app.modules.film.application.service.load_film import load_film_id
from app.modules.film.domain.film.entity import Film, FilmId
from app.uow.swapi_uow import SqlSwapiUoW


def film_from_dict(film_data: dict[str, Any]) -> Film:
    id = id_from_url(film_data.get("url"))
    return Film(
        id=FilmId(value=id),
        title=film_data["title"],
        episode_id=film_data["episode_id"],
        opening_crawl=film_data.get("opening_crawl"),
        director=film_data.get("director"),
        producer=film_data.get("producer"),
        release_date=film_data.get("release_date"),
        swapi_url=film_data.get("url"),
    )


def register_films(
        films: list[dict[str, Any]],
        uow: SqlSwapiUoW
        ) -> List[Film]:

    with uow:
        registered = []

        for film_data in films:
            film_id = id_from_url(film_data.get("url"))
            film_id = load_film_id(uow.film_repo, film_id)
            if film_id:
                continue
            film = film_from_dict(film_data)
            uow.film_repo.register_film(film)
            registered.append(film)

        return registered
