from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.starship.domain.repo.starship_repo import StarshipRepoI
from app.modules.starship.domain.starship.entity import Starship
from app.modules.starship.infrastructure.persistance.sql_queries.starship_query import (
    get_films_for_starship_query,
    get_pilots_for_starship_query,
    get_starship_query,
    get_starships_paginated_query,
    insert_starship_query,
    link_starship_character_query,
    link_starship_film_query,
    search_starships_by_name_query,
)


class SqlStarshipRepo(StarshipRepoI, SqlBaseRepository):

    def register_starship(self, starship: Starship) -> Starship:
        query, params = insert_starship_query(starship)
        SqlQuery(self.session, query, params).persist()
        return starship

    def link_starship_film(self, starship_id: int, film_id: int) -> None:
        query, params = link_starship_film_query(starship_id, film_id)
        SqlQuery(self.session, query, params).persist()

    def link_starship_character(self, starship_id: int, character_id: int) -> None:
        query, params = link_starship_character_query(starship_id, character_id)
        SqlQuery(self.session, query, params).persist()

    def load_starship_id(self, starship_id: int) -> int:
        query, params = get_starship_query(starship_id)
        return SqlQuery(self.session, query, params).fetch_one()

    def search_starship(self, name: str) -> list:
        query, params = search_starships_by_name_query(name)
        return SqlQuery(self.session, query, params).fetch_all()

    def get_starships(self, limit: int, offset: int) -> list[dict]:
        query, params = get_starships_paginated_query(limit, offset)
        return SqlQuery(self.session, query, params).fetch_all()

    def get_films_for_starship(self, starship_id: int) -> list[dict]:
        query, params = get_films_for_starship_query(starship_id)
        return SqlQuery(self.session, query, params).fetch_all()

    def get_pilots_for_starship(self, starship_id: int) -> list[dict]:
        query, params = get_pilots_for_starship_query(starship_id)
        return SqlQuery(self.session, query, params).fetch_all()
