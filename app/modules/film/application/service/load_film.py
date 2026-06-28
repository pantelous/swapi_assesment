from sqlalchemy.orm import Session

from app.core.exception import ApplicationException
from app.modules.film.domain.film.entity import Film
from app.modules.film.domain.repo.film_repo import FilmRepoI


def load_film_id(film_repo: FilmRepoI, film_id: int) -> dict[str, int]:
    return film_repo.load_film_id(film_id)

def load_film_by_name(film_repo: FilmRepoI, film_name: str) -> Film:
    film = film_repo.get_film_by_name(film_name)
    if not film:
        raise ApplicationException(field='film', message=f"The movie with the name {film_name} not found.", type='not_found')
    return film
