from typing import Any, List

from app.core.db_session import SessionManager
from app.modules.character.application.service.load_character import load_character_id
from app.modules.character.domain.character.entity import Character, CharacterId
from app.modules.character.domain.repo.character_repo import CharacterRepoI


def id_from_url(url: str) -> int:
    id = url.rstrip("/").split("/")[-1]
    try:
        return int(id)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot extract ID from URL: {url}")


def character_from_dict(char_data: dict[str, Any]) -> Character:
    id = id_from_url(char_data.get("url"))
    return Character(
        id=CharacterId(value=id),
        name=char_data["name"],
        height=char_data.get("height"),
        mass=char_data.get("mass"),
        hair_color=char_data.get("hair_color"),
        skin_color=char_data.get("skin_color"),
        eye_color=char_data.get("eye_color"),
        birth_year=char_data.get("birth_year"),
        gender=char_data.get("gender"),
        homeworld=char_data.get("homeworld"),
        swapi_url=char_data.get("url"),
        films=char_data.get("films", []),
    )


def register_characters(
        characters: list[dict[str, Any]],
        repo: CharacterRepoI,
        session_scope=SessionManager.session_scope
    ) -> List[Character]:

    with session_scope() as session:
        registered = []

        for char_data in characters:
            character_id = id_from_url(char_data.get("url"))
            character_id = load_character_id(session, repo, character_id)
            if character_id:
                continue
            character = character_from_dict(char_data)
            
            repo.register_character(session, character)

            swapi_character_id = id_from_url(char_data["url"])
            for film_url in char_data.get("films", []):
                swapi_film_id = id_from_url(film_url)
                repo.link_character_film(session, swapi_character_id, swapi_film_id)

            registered.append(character)
        return registered
