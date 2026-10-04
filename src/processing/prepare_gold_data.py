
from pyspark.sql.functions import (
    col,
    xxhash64,
    concat_ws
)


def prepare_dim_location(df):
    """
    Prepare location dimension data.
    """

    # Remove rows where location information is missing
    dim_location = (
        df
        .filter(
            col("district").isNotNull() &
            col("latitude").isNotNull() &
            col("longitude").isNotNull()
        )
        .select(
            "district",
            "latitude",
            "longitude",
            "timezone"
        )
        .dropDuplicates([
            "district",
            "latitude",
            "longitude",
            "timezone"
        ])
        .withColumn(
            "location_id",
            xxhash64(
                "district",
                "latitude",
                "longitude",
                "timezone"
            )
        )
        .select(
            "location_id",
            "district",
            "latitude",
            "longitude",
            "timezone"
        )
    )

    return dim_location


def prepare_fact_weather(df, dim_location):
    """
    Prepare weather fact data by joining it with dim_location.
    """

    fact_weather = (
        df
        .join(
            dim_location,
            on=[
                "district",
                "latitude",
                "longitude",
                "timezone"
            ],
            how="left"
        )
        .withColumn(
            "weather_id",
            xxhash64(
                concat_ws(
                    "|",
                    "district",
                    "latitude",
                    "longitude",
                    "time"
                )
            )
        )
        .select(
            "weather_id",
            "location_id",
            "time",
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "cloud_cover",
            "pressure_msl",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m"
        )
    )

    return fact_weather
