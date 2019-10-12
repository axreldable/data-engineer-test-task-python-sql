CREATE TABLE IF NOT EXISTS locations
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    country_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tweets
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    text        TEXT     NOT NULL,
    sentiment   INTEGER  NOT NULL,
    lang        TEXT     NOT NULL,
    created_at  DATETIME NOT NULL,
    location_id INTEGER,
    user_id     INTEGER  NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE VIEW tweets_for_insert AS
SELECT tweets.text,
       tweets.lang,
       tweets.sentiment,
       tweets.created_at,
       locations.name         AS location_name,
       locations.country_code AS country_code,
       users.name             AS user_name
FROM tweets
         INNER JOIN locations ON tweets.location_id = locations.id
         INNER JOIN users on tweets.user_id = users.id;


CREATE TRIGGER insert_tweets
    INSTEAD OF INSERT
    ON tweets_for_insert

BEGIN

    INSERT INTO locations (name, country_code)
    SELECT NEW.location_name, NEW.country_code
    WHERE NOT EXISTS
        (SELECT 1, 2
         FROM locations
         WHERE name = NEW.location_name
           AND country_code = NEW.country_code)
      AND NEW.location_name IS NOT NULL
      AND NEW.country_code IS NOT NULL;

    INSERT INTO users (name)
    SELECT NEW.user_name
    WHERE NOT EXISTS
        (SELECT 1
         FROM users
         WHERE name = NEW.user_name);

    INSERT INTO tweets (text, lang, sentiment, created_at, location_id, user_id)
    SELECT NEW.text,
           NEW.lang,
           NEW.sentiment,
           NEW.created_at,
           (select locations.id
            from locations
            where locations.name = NEW.location_name
              and locations.country_code = NEW.country_code),
           (select users.id from users where users.name = NEW.user_name);

END;
