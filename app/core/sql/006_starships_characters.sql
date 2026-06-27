CREATE TABLE IF NOT EXISTS starships_characters (
    starship_id  INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    PRIMARY KEY (starship_id, character_id),
    FOREIGN KEY (starship_id)  REFERENCES starships  (id) ON DELETE CASCADE,
    FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE
);
