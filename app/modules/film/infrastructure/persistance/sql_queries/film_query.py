from typing import Any

from app.core.protocol import get_value
from app.modules.film.domain.film.entity import Film


def get_film_query(film_id: int) -> tuple[str, dict]:
    query = """
        SELECT f.id
          FROM films f
         WHERE f.id = :film_id
    """
    params = {"film_id": film_id}
    return query, params


def insert_film_query(film: Film) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO films (
                id,
                title,
                episode_id,
                opening_crawl,
                director,
                producer,
                release_date,
                swapi_url)
        VALUES (
                :id,
                :title,
                :episode_id,
                :opening_crawl,
                :director,
                :producer,
                :release_date,
                :swapi_url)
    """
    params = {
        'id': get_value(film.id),
        'title': film.title,
        'episode_id': film.episode_id,
        'opening_crawl': film.opening_crawl,
        'director': film.director,
        'producer': film.producer,
        'release_date': film.release_date,
        'swapi_url': film.swapi_url,
    }
    return query, params
