from pydantic import BaseModel

from app.modules.film.application.service.load_film import load_film_by_name
from app.modules.film.domain.film.entity import Film
from app.uow.swapi_uow import SwapiUoWI

class VoteFilmQuery(BaseModel):
    name: str

def vote_film(
        uow: SwapiUoWI,
        query_params: VoteFilmQuery,
) -> list[dict[str, Film]]:

    with uow:
        film: Film = load_film_by_name(uow.film_repo, query_params.name)
        votes = film.votes

        film = film.model_copy(
            update={"votes": 1 if not votes else votes + 1}
        )

        uow.film_repo.update_film_votes(film)
        
        uow.commit()
        return film
