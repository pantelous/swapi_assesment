from app.modules.film.domain.film.entity import Film, FilmId


def transform_film_data(film_data: dict | None) -> Film | None:
    if film_data is None:
        return None

    film = Film.model_construct(
        id=FilmId(value=film_data["id"]),
        title=film_data["title"],
        episode_id=film_data["episode_id"],
        opening_crawl=film_data.get("opening_crawl"),
        director=film_data.get("director"),
        producer=film_data.get("producer"),
        release_date=film_data.get("release_date"),
        swapi_url=film_data.get("swapi_url"),
        votes=film_data.get("votes"),
        starships=film_data.get("starships", []),
    )

    return film
