CREATE TABLE IF NOT EXISTS characters_films (
    character_id INTEGER NOT NULL,
    film_id      INTEGER NOT NULL,
    PRIMARY KEY (character_id, film_id),
    FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE,
    FOREIGN KEY (film_id) REFERENCES films (id) ON DELETE CASCADE
);
