from typing import Any

from app.core.protocol import get_value
from app.modules.film.domain.film.entity import Film


def search_films_by_title_query(title: str) -> tuple[str, dict]:
    query = """
        SELECT id,
               title,
               episode_id,
               opening_crawl,
               director,
               producer,
               release_date,
               votes,
               swapi_url
          FROM films
         WHERE title LIKE :title
         ORDER BY episode_id
    """
    params = {"title": f"%{title}%"}
    return query, params


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

def get_films_paginated_query(limit: int, offset: int) -> tuple[str, dict]:
    query = """
        SELECT id,
               title,
               episode_id,
               opening_crawl,
               director,
               producer,
               release_date,
               swapi_url,
               votes
          FROM films
         ORDER BY episode_id
         LIMIT :limit OFFSET :offset
    """
    params = {"limit": limit, "offset": offset}
    return query, params

def get_film_by_name_query(film_name: str) -> tuple[str, dict]:
    query = """
        SELECT id,
               title,
               episode_id,
               opening_crawl,
               director,
               producer,
               release_date,
               swapi_url,
               votes
          FROM films
          WHERE title = :title
    """
    params = {"title": film_name}
    return query, params


def link_film_starship_query(film_id: int, starship_id: int) -> tuple[str, dict]:
    query = """
        INSERT INTO starships_films (starship_id, film_id)
        VALUES (:starship_id, :film_id)
    """
    return query, {"film_id": film_id, "starship_id": starship_id}


def get_characters_for_film_query(film_id: int) -> tuple[str, dict]:
    query = """
        SELECT ch.id,
               ch.name,
               ch.height,
               ch.mass,
               ch.hair_color,
               ch.skin_color,
               ch.eye_color,
               ch.birth_year,
               ch.gender,
               ch.homeworld,
               ch.swapi_url
           FROM characters ch
          JOIN characters_films cf ON cf.character_id = ch.id
         WHERE cf.film_id = :film_id
         ORDER BY ch.id
    """
    params = {"film_id": film_id}
    return query, params

def update_film_votes_query(film: Film) -> tuple[str, dict[str, Any]]:

    query = """
        UPDATE films
        SET votes = :votes
        WHERE id = :film_id
"""

    params = {
            'film_id': get_value(film.id),
            'votes': film.votes,
    }
    
    return query, params