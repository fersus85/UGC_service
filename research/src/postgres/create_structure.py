from typing import Dict, cast, Any

import psycopg
from postgres.connection_info import pg_dsl


def initialize_db(dsl: Dict[str, str | None]) -> None:
    with psycopg.connect(**cast(Any, dsl)) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                " id UUID PRIMARY KEY, "
                " created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), "
                " login TEXT NOT NULL, "
                " password_hash TEXT NOT NULL, "
                " first_name TEXT, "
                " last_name TEXT"
                ");"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS movies ("
                " id UUID PRIMARY KEY, "
                " title TEXT NOT NULL, "
                " description TEXT, "
                " creation_date DATE, "
                " rating FLOAT, "
                " type TEXT NOT NULL, "
                " created TIMESTAMPTZ NOT NULL DEFAULT NOW(), "
                " modified TIMESTAMPTZ NOT NULL DEFAULT NOW()"
                ");"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS ratings ("
                " movie_id UUID NOT NULL "
                "REFERENCES movies(id) ON DELETE CASCADE, "
                " user_id UUID NOT NULL "
                "REFERENCES users(id) ON DELETE CASCADE, "
                " rating SMALLINT NOT NULL "
                "CHECK (rating >= 0 AND rating <= 10), "
                " created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()"
                ");"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS favorites ("
                " movie_id UUID NOT NULL "
                "REFERENCES movies(id) ON DELETE CASCADE, "
                " user_id UUID NOT NULL "
                "REFERENCES users(id) ON DELETE CASCADE, "
                " created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), "
                " PRIMARY KEY (user_id, movie_id)"
                ");"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS reviews ("
                " id UUID PRIMARY KEY, "
                " movie_id UUID NOT NULL "
                "REFERENCES movies(id) ON DELETE CASCADE, "
                " user_id UUID NOT NULL "
                "REFERENCES users(id) ON DELETE CASCADE, "
                " review_text TEXT NOT NULL, "
                " created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()"
                ");"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS review_likes ("
                " id UUID PRIMARY KEY, "
                " review_id UUID NOT NULL "
                "REFERENCES reviews(id) ON DELETE CASCADE, "
                " user_id UUID NOT NULL "
                "REFERENCES users(id) ON DELETE CASCADE, "
                " is_like BOOLEAN NOT NULL, "
                " created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()"
                ");"
            )
            conn.commit()


if __name__ == "__main__":
    initialize_db(pg_dsl)
