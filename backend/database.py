
import psycopg2

from config.config import (
    JDBC_USER,
    JDBC_PASSWORD
)


DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "weather_db"


def get_connection():

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=JDBC_USER,
        password=JDBC_PASSWORD
    )
