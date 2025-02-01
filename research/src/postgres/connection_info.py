import os

from dotenv import load_dotenv

load_dotenv()

pg_dsl = {
    "dbname": os.getenv("POSTGRES_DBNAME", "postgres"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}
