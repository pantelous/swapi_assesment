from sqlalchemy.orm import Session

from app.modules.film.domain.repo.film_repo import FilmRepoI


def load_film_id(session: Session, film_repo: FilmRepoI, film_id: int) -> dict[str, int]:
    return film_repo.load_film_id(session, film_id)
