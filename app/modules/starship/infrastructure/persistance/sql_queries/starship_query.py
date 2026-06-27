from typing import Any

from app.core.protocol import get_value
from app.modules.starship.domain.starship.entity import Starship


def insert_starship_query(starship: Starship) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO starships (
                id,
                name,
                model,
                manufacturer,
                cost_in_credits,
                length,
                max_atmosphering_speed,
                crew,
                passengers,
                cargo_capacity,
                consumables,
                hyperdrive_rating,
                mglt,
                starship_class,
                swapi_url)
        VALUES (
                :id,
                :name,
                :model,
                :manufacturer,
                :cost_in_credits,
                :length,
                :max_atmosphering_speed,
                :crew,
                :passengers,
                :cargo_capacity,
                :consumables,
                :hyperdrive_rating,
                :mglt,
                :starship_class,
                :swapi_url)
    """
    params = {
        'id': get_value(starship.id),
        'name': starship.name,
        'model': starship.model,
        'manufacturer': starship.manufacturer,
        'cost_in_credits': starship.cost_in_credits,
        'length': starship.length,
        'max_atmosphering_speed': starship.max_atmosphering_speed,
        'crew': starship.crew,
        'passengers': starship.passengers,
        'cargo_capacity': starship.cargo_capacity,
        'consumables': starship.consumables,
        'hyperdrive_rating': starship.hyperdrive_rating,
        'mglt': starship.mglt,
        'starship_class': starship.starship_class,
        'swapi_url': starship.swapi_url,
    }
    return query, params


def get_starship_query(starship_id: int) -> tuple[str, dict]:
    query = """
        SELECT s.id
          FROM starships s
         WHERE s.id = :starship_id
    """
    return query, {"starship_id": starship_id}


def link_starship_film_query(starship_id: int, film_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO starships_films (starship_id, film_id)
        VALUES (:starship_id, :film_id)
    """
    return query, {"starship_id": starship_id, "film_id": film_id}


def link_starship_character_query(starship_id: int, character_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO starships_characters (starship_id, character_id)
        VALUES (:starship_id, :character_id)
    """
    return query, {"starship_id": starship_id, "character_id": character_id}


def search_starships_by_name_query(name: str) -> tuple[str, dict]:
    query = """
        SELECT id,
               name,
               model,
               manufacturer,
               cost_in_credits,
               length,
               max_atmosphering_speed,
               crew,
               passengers,
               cargo_capacity,
               consumables,
               hyperdrive_rating,
               mglt,
               starship_class,
               swapi_url
          FROM starships
         WHERE name LIKE :name
         ORDER BY name
    """
    return query, {"name": f"%{name}%"}


def get_starships_paginated_query(limit: int, offset: int) -> tuple[str, dict]:
    query = """
        SELECT id,
               name,
               model,
               manufacturer,
               cost_in_credits,
               length,
               max_atmosphering_speed,
               crew,
               passengers,
               cargo_capacity,
               consumables,
               hyperdrive_rating,
               mglt,
               starship_class,
               swapi_url
          FROM starships
         ORDER BY id
         LIMIT :limit OFFSET :offset
    """
    return query, {"limit": limit, "offset": offset}


def get_films_for_starship_query(starship_id: int) -> tuple[str, dict]:
    query = """
        SELECT f.id,
               f.title,
               f.episode_id,
               f.opening_crawl,
               f.director,
               f.producer,
               f.release_date,
               f.swapi_url
          FROM films f
          JOIN starships_films sf ON sf.film_id = f.id
         WHERE sf.starship_id = :starship_id
         ORDER BY f.episode_id
    """
    return query, {"starship_id": starship_id}


def get_pilots_for_starship_query(starship_id: int) -> tuple[str, dict]:
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
          JOIN starships_characters sc ON sc.character_id = ch.id
         WHERE sc.starship_id = :starship_id
         ORDER BY ch.id
    """
    return query, {"starship_id": starship_id}
