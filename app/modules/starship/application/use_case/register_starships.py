from typing import Any, List

from app.modules.character.application.use_case.register_characters import id_from_url
from app.modules.starship.application.service.load_starship import load_starship_id
from app.modules.starship.domain.starship.entity import Starship, StarshipId
from app.uow.swapi_uow import SwapiUoWI


def starship_from_dict(starship_data: dict[str, Any]) -> Starship:
    id = id_from_url(starship_data.get("url"))
    return Starship(
        id=StarshipId(value=id),
        name=starship_data["name"],
        model=starship_data.get("model"),
        manufacturer=starship_data.get("manufacturer"),
        cost_in_credits=starship_data.get("cost_in_credits"),
        length=starship_data.get("length"),
        max_atmosphering_speed=starship_data.get("max_atmosphering_speed"),
        crew=starship_data.get("crew"),
        passengers=starship_data.get("passengers"),
        cargo_capacity=starship_data.get("cargo_capacity"),
        consumables=starship_data.get("consumables"),
        hyperdrive_rating=starship_data.get("hyperdrive_rating"),
        mglt=starship_data.get("MGLT"),
        starship_class=starship_data.get("starship_class"),
        swapi_url=starship_data.get("url"),
        films=starship_data.get("films", []),
        pilots=starship_data.get("pilots", []),
    )


def register_starships(
    starships: list[dict[str, Any]],
    uow: SwapiUoWI,
) -> List[Starship]:

    with uow:
        registered = []

        for starship_data in starships:
            starship_id = id_from_url(starship_data.get("url"))
            existing = load_starship_id(uow.starship_repo, starship_id)
            if existing:
                continue

            starship = starship_from_dict(starship_data)
            uow.starship_repo.register_starship(starship)


            for pilot_url in starship_data.get("pilots", []):
                character_id = id_from_url(pilot_url)
                uow.starship_repo.link_starship_character(starship_id, character_id)

            registered.append(starship)

        return registered
