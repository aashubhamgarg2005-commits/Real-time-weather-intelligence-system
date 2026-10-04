
from config.config import (
    JDBC_URL,
    JDBC_USER,
    JDBC_PASSWORD,
    JDBC_DRIVER
)

from .prepare_gold_data import (
    prepare_dim_location,
    prepare_fact_weather
)

from .spark_session import spark


def get_connection():
    """
    Create PostgreSQL JDBC connection.
    """

    return spark._sc._gateway.jvm.java.sql.DriverManager.getConnection(
        JDBC_URL,
        JDBC_USER,
        JDBC_PASSWORD
    )


def write_to_database(batch_df, batch_id):

    properties = {
        "user": JDBC_USER,
        "password": JDBC_PASSWORD,
        "driver": JDBC_DRIVER
    }

    connection = None
    statement = None

    try:

        # ==================================================
        # 1. Prepare dimension data
        # ==================================================

        dim_location_df = prepare_dim_location(batch_df)

        # ==================================================
        # 2. Clear current staging table
        # ==================================================

        connection = get_connection()
        statement = connection.createStatement()

        statement.executeUpdate(
            "TRUNCATE TABLE staging_dim_location"
        )

        # ==================================================
        # 3. Write current batch to staging
        # ==================================================

        dim_location_df.write.jdbc(
            url=JDBC_URL,
            table="staging_dim_location",
            mode="append",
            properties=properties
        )

        # ==================================================
        # 4. Insert new locations
        #    Existing location_id will be ignored
        # ==================================================

        statement.executeUpdate("""
            INSERT INTO dim_location (
                location_id,
                district,
                latitude,
                longitude,
                timezone
            )
            SELECT
                location_id,
                district,
                latitude,
                longitude,
                timezone
            FROM staging_dim_location
            ON CONFLICT (location_id) DO NOTHING
        """)

        # ==================================================
        # 5. Prepare fact data
        # ==================================================

        fact_weather_df = prepare_fact_weather(
            batch_df,
            dim_location_df
        )

        # ==================================================
        # 6. Clear fact staging table
        # ==================================================

        statement.executeUpdate(
            "TRUNCATE TABLE staging_fact_weather"
        )

        # ==================================================
        # 7. Write current batch to fact staging
        # ==================================================

        fact_weather_df.write.jdbc(
            url=JDBC_URL,
            table="staging_fact_weather",
            mode="append",
            properties=properties
        )

        # ==================================================
        # 8. Insert new weather records
        #    Existing weather_id will be ignored
        # ==================================================

        statement.executeUpdate("""
            INSERT INTO fact_weather (
                weather_id,
                location_id,
                time,
                temperature_2m,
                relative_humidity_2m,
                apparent_temperature,
                precipitation,
                rain,
                showers,
                snowfall,
                cloud_cover,
                pressure_msl,
                wind_speed_10m,
                wind_direction_10m,
                wind_gusts_10m
            )
            SELECT
                weather_id,
                location_id,
                time,
                temperature_2m,
                relative_humidity_2m,
                apparent_temperature,
                precipitation,
                rain,
                showers,
                snowfall,
                cloud_cover,
                pressure_msl,
                wind_speed_10m,
                wind_direction_10m,
                wind_gusts_10m
            FROM staging_fact_weather
            ON CONFLICT (weather_id) DO NOTHING
        """)

        print(f"Batch {batch_id} inserted successfully.")

    except Exception as e:

        print(f"Error in batch {batch_id}: {e}")
        raise

    finally:

        if statement is not None:
            statement.close()

        if connection is not None:
            connection.close()
