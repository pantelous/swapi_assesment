from sqlalchemy.orm import Session

from app.modules.film.domain.film.entity import Film
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.core.sql_query import SqlQuery
from app.modules.film.infrastructure.persistance.sql_queries.film_query import get_film_query, insert_film_query


class SqlFilmRepo(FilmRepoI):

    def register_film(self,session: Session, film: Film) -> Film:
        query, params = insert_film_query(film)
        SqlQuery(session, query, params).persist()
        return film

    def load_film_id(self, session: Session, film_id: int) -> None:
        query, params = get_film_query(film_id)
        return SqlQuery(session, query, params).fetch_one()
