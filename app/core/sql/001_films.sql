CREATE TABLE IF NOT EXISTS films (
    id          INTEGER PRIMARY KEY,
    title         VARCHAR(255) NOT NULL,
    episode_id    INTEGER      UNIQUE NOT NULL,
    opening_crawl TEXT,
    director      VARCHAR(255),
    producer      VARCHAR(255),
    release_date  DATE,
    swapi_url     VARCHAR(255) UNIQUE,
    votes         INTEGER      NOT NULL DEFAULT 0,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
