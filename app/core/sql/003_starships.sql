CREATE TABLE IF NOT EXISTS starships (
    id                     INTEGER PRIMARY KEY,
    name                   VARCHAR(255) NOT NULL,
    model                  VARCHAR(255),
    manufacturer           VARCHAR(255),
    cost_in_credits        VARCHAR(50),
    length                 VARCHAR(50),
    max_atmosphering_speed VARCHAR(50),
    crew                   VARCHAR(50),
    passengers             VARCHAR(50),
    cargo_capacity         VARCHAR(50),
    consumables            VARCHAR(100),
    hyperdrive_rating      VARCHAR(50),
    mglt                   VARCHAR(50),
    starship_class         VARCHAR(100),
    swapi_url              VARCHAR(255) UNIQUE,
    created_at             TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
