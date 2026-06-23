CREATE TABLE IF NOT EXISTS characters (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    height      VARCHAR(50),
    mass        VARCHAR(50),
    hair_color  VARCHAR(100),
    skin_color  VARCHAR(100),
    eye_color   VARCHAR(100),
    birth_year  VARCHAR(50),
    gender      VARCHAR(50),
    homeworld   VARCHAR(255),
    swapi_url   VARCHAR(255) UNIQUE,
    votes       INTEGER      NOT NULL DEFAULT 0,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
