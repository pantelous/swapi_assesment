CREATE TABLE IF NOT EXISTS character_starships (
    character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    starship_id  INTEGER NOT NULL REFERENCES starships(id)  ON DELETE CASCADE,
    PRIMARY KEY (character_id, starship_id)
);
