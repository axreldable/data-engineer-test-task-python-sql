CREATE TABLE IF NOT EXISTS countries
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS locations
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries (id)
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
       locations.name AS location_name,
       countries.name AS country_name,
       countries.code AS country_code,
       users.name     AS user_name
FROM tweets
         INNER JOIN locations ON tweets.location_id = locations.id
         INNER JOIN countries ON locations.country_id = countries.id
         INNER JOIN users ON tweets.user_id = users.id;


CREATE TRIGGER insert_tweets
    INSTEAD OF INSERT
    ON tweets_for_insert

BEGIN

    INSERT INTO countries (name, code)
    SELECT NEW.country_name, NEW.country_code
    WHERE NOT EXISTS
        (SELECT 1, 2
         FROM countries
         WHERE name = NEW.country_name
           AND code = NEW.country_code)
      AND NEW.country_name IS NOT NULL
      AND NEW.country_code IS NOT NULL;

    INSERT INTO locations (name, country_id)
    SELECT NEW.location_name,
           (select countries.id from countries where name = NEW.country_name and code = NEW.country_code)
    WHERE NOT EXISTS
        (SELECT 1, 2
         FROM locations
                  INNER JOIN countries
                             ON locations.country_id = countries.id
         WHERE locations.name = NEW.location_name
           AND countries.name = NEW.country_name
           AND countries.code = NEW.country_code)
      AND NEW.location_name IS NOT NULL;

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
                     inner join countries on locations.country_id = countries.id
            where locations.name = NEW.location_name
              and countries.name = NEW.country_name
              and countries.code = NEW.country_code),
           (select users.id from users where users.name = NEW.user_name);

END;
