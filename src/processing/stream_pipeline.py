from .spark_session import spark
from config.logging import logger
from .Read_stream_data import raw_stream_df
from .transform_data import transform_weather_data
import traceback


def main():
    try:
        bronze_df = raw_stream_df.selectExpr(
            "CAST(key AS STRING) AS key",
            "CAST(value AS STRING) AS value",
            "topic",
            "partition",
            "offset",
            "timestamp",
            "timestampType"
        )

        bronze_query = (
            bronze_df.writeStream
            .format("json")
            .option(
                "path",
                "file:///C:/Users/HP/OneDrive/Desktop/weather/data/Bronze"
            )
            .option(
                "checkpointLocation",
                "file:///C:/Users/HP/OneDrive/Desktop/weather/checkpoint"
            )
            .outputMode("append")
            .start()
        )

        logger.info("Spark streaming started successfully.")
        #query.awaitTermination()

    except Exception as e:
        logger.error(f"Error occurred while writing stream data: {e}")
        logger.error(traceback.format_exc())
        raise

    try:
        # Transform the weather data
        transformed_df = transform_weather_data(bronze_df)
        # Write the transformed data to the process layer
        silver_query = (
            transformed_df.writeStream
            .format("parquet")
            .option(
                "path",
                "file:///C:/Users/HP/OneDrive/Desktop/weather/data/process"
            )
            .option(
                "checkpointLocation",
                "file:///C:/Users/HP/OneDrive/Desktop/weather/checkpoint_process"
            )
            .outputMode("append")
            .start()
        )

        logger.info("Transformed data written to Silver layer successfully.")
        spark.streams.awaitAnyTermination()
    except Exception as e:
        logger.error(f"Error occurred while transforming and writing stream data: {e}")
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()