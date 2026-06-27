CREATE TABLE IF NOT EXISTS starships_films (
    starship_id INTEGER NOT NULL,
    film_id     INTEGER NOT NULL,
    PRIMARY KEY (starship_id, film_id),
    FOREIGN KEY (starship_id) REFERENCES starships (id) ON DELETE CASCADE,
    FOREIGN KEY (film_id)     REFERENCES films (id)     ON DELETE CASCADE
);
