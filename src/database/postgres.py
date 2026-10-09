from src.processing.spark_session import spark

from config.config import (
    JDBC_URL,
    JDBC_PASSWORD,
    JDBC_USER,
    JDBC_DRIVER
)


def get_jdbc_properties():

    return {
        "user": JDBC_USER,
        "password": JDBC_PASSWORD,
        "driver": JDBC_DRIVER
    }


def read_table(table_name):

    properties = get_jdbc_properties()

    return spark.read.jdbc(
        url=JDBC_URL,
        table=table_name,
        properties=properties
    )