CREATE TABLE IF NOT EXISTS character_films (
    character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    film_id      INTEGER NOT NULL REFERENCES films(id)      ON DELETE CASCADE,
    PRIMARY KEY (character_id, film_id)
);
