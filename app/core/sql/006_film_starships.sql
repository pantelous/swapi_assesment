CREATE TABLE IF NOT EXISTS film_starships (
    film_id     INTEGER NOT NULL REFERENCES films(id)     ON DELETE CASCADE,
    starship_id INTEGER NOT NULL REFERENCES starships(id) ON DELETE CASCADE,
    PRIMARY KEY (film_id, starship_id)
);
