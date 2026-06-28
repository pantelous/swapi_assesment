from sqlalchemy.orm import Session

from app.core.base_repository import SqlBaseRepository
from app.modules.film.domain.film.entity import Film
from app.modules.film.domain.repo.film_repo import FilmRepoI
from app.core.sql_query import SqlQuery
from app.modules.film.infrastructure.persistance.sql_queries.film_query import get_characters_for_film_query, get_film_by_name_query, get_film_query, get_films_paginated_query, insert_film_query, link_film_starship_query, search_films_by_title_query, update_film_votes_query
from app.modules.film.infrastructure.transformers.film_transformer import transform_film_data


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
    
    def get_film_by_name(self, film_name: str) -> Film:
        query, params = get_film_by_name_query(film_name)
        return SqlQuery(self.session, query, params).fetch_one(transformer=transform_film_data)

    def get_characters_for_film(self, film_id: int) -> list[dict]:
        query, params = get_characters_for_film_query(film_id)
        sql_query = SqlQuery(self.session, query, params)
        return sql_query.fetch_all()

    def link_film_starship(self, film_id: int, starship_id: int) -> None:
        query, params = link_film_starship_query(film_id, starship_id)
        SqlQuery(self.session, query, params).persist()

    def update_film_votes(self, film: Film) -> Film:
        query, params = update_film_votes_query(film)
        sql_query = SqlQuery(self.session, query, params)
        sql_query.persist()
        return film
        
