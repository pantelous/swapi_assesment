from sqlalchemy.orm import Session

from app.core.base_repository import SqlBaseRepository
from app.modules.film.domain.film.entity import Film
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.core.sql_query import SqlQuery
from app.modules.film.infrastructure.persistance.sql_queries.film_query import get_characters_for_film_query, get_film_query, get_films_paginated_query, insert_film_query, link_film_starship_query, search_films_by_title_query


class SqlFilmRepo(FilmRepoI, SqlBaseRepository):

    def register_film(self, film: Film) -> Film:
        query, params = insert_film_query(film)
        SqlQuery(self.session, query, params).persist()
        return film

    def load_film_id(self, film_id: int) -> None:
        query, params = get_film_query(film_id)
        return SqlQuery(self.session, query, params).fetch_one()

    def search_film(self, title: str) -> list:
        query, params = search_films_by_title_query(title)
        return SqlQuery(self.session, query, params).fetch_all()
    
    
    def get_films(self, limit: int, offset: int) -> list[dict]:
        query, params = get_films_paginated_query(limit, offset)
        return SqlQuery(self.session, query, params).fetch_all()

    def get_characters_for_film(self, film_id: int) -> list[dict]:
        query, params = get_characters_for_film_query(film_id)
        sql_query = SqlQuery(self.session, query, params)
        return sql_query.fetch_all()

    def link_film_starship(self, film_id: int, starship_id: int) -> None:
        query, params = link_film_starship_query(film_id, starship_id)
        SqlQuery(self.session, query, params).persist()
        
