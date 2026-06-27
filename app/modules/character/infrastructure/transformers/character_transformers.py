from app.modules.character.domain.character.entity import Character, CharacterId


def transform_character_data(character_data: dict | None) -> Character | None:
    if character_data is None:
        return None

    character = Character.model_construct(
        id=CharacterId(value=character_data["id"]),
        name=character_data["name"],
        height=character_data.get("height"),
        mass=character_data.get("mass"),
        hair_color=character_data.get("hair_color"),
        skin_color=character_data.get("skin_color"),
        eye_color=character_data.get("eye_color"),
        birth_year=character_data.get("birth_year"),
        gender=character_data.get("gender"),
        homeworld=character_data.get("homeworld"),
        swapi_url=character_data.get("swapi_url"),
        films=character_data.get("films", []),
    )

    return character