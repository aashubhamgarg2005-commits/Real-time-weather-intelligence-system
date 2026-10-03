from pyspark.sql.functions import *
from src.processing.weather_schema import weather_schema


def transform_weather_data(df):
    json_df = df.withColumn(
    "value",
    regexp_replace("value", "'", '"')
)

    parsed_df = json_df.withColumn(
        "value",
        from_json(col("value"), weather_schema)
    )

    transform_df = parsed_df.select(
        col("value.district").cast("string").alias("district"),
        col("value.latitude").cast("double").alias("latitude"),
        col("value.longitude").cast("double").alias("longitude"),
        col("value.weather.timezone").cast("string").alias("timezone"),
        to_timestamp(col("value.weather.current.time"), "yyyy-MM-dd'T'HH:mm").alias("time"),
        col("value.weather.current.temperature_2m").cast("double").alias("temperature_2m"),
        col("value.weather.current.relative_humidity_2m").cast("double").alias("relative_humidity_2m"),
        col("value.weather.current.apparent_temperature").cast("double").alias("apparent_temperature"),
        col("value.weather.current.precipitation").cast("double").alias("precipitation"),
        col("value.weather.current.rain").cast("double").alias("rain"),
        col("value.weather.current.showers").cast("double").alias("showers"),
        col("value.weather.current.snowfall").cast("double").alias("snowfall"),
        col("value.weather.current.cloud_cover").cast("double").alias("cloud_cover"),
        col("value.weather.current.pressure_msl").cast("double").alias("pressure_msl"),
        col("value.weather.current.wind_speed_10m").cast("double").alias("wind_speed_10m"),
        col("value.weather.current.wind_direction_10m").cast("double").alias("wind_direction_10m"),
        col("value.weather.current.wind_gusts_10m").cast("double").alias("wind_gusts_10m")
    )

    return transform_df