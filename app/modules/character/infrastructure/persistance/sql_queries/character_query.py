from typing import Any

from app.core.protocol import get_value
from app.modules.character.domain.character.entity import Character


def search_characters_by_name_query(name: str) -> tuple[str, dict[str, Any]]:
    query = """
        SELECT id,
               name,
               height,
               mass,
               hair_color,
               skin_color,
               eye_color,
               birth_year,
               gender,
               homeworld,
               swapi_url
          FROM characters
         WHERE name LIKE :name
         ORDER BY name
    """
    params = {"name": f"%{name}%"}
    return query, params


def insert_character_query(character: Character) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO characters (
                id,
                name,
                height,
                mass,
                hair_color,
                skin_color,
                eye_color,
                birth_year,
                gender,
                homeworld,
                swapi_url)
        VALUES (
                :id,
                :name,
                :height,
                :mass,
                :hair_color,
                :skin_color,
                :eye_color,
                :birth_year,
                :gender,
                :homeworld,
                :swapi_url)
    """

    params = {
        'id': get_value(character.id),
        'name': character.name,
        'height': character.height,
        'mass': character.mass,
        'hair_color': character.hair_color,
        'skin_color': character.skin_color,
        'eye_color': character.eye_color,
        'birth_year': character.birth_year,
        'gender': character.gender,
        'homeworld': character.homeworld,
        'swapi_url': character.swapi_url,
    }

    return query, params


def link_character_film_query(swapi_character_id: int, swapi_film_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO characters_films (character_id, film_id)
        VALUES (:swapi_character_id, :swapi_film_id)
    """
    return query, {"swapi_character_id": swapi_character_id, "swapi_film_id": swapi_film_id}

def get_character_query(character_id: int) -> tuple[str, dict]:
    query = """
        SELECT ch.id
          FROM characters ch
         WHERE ch.id = :character_id
    """
    params = {"character_id": character_id}
    return query, params