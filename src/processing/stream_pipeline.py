
from .spark_session import spark
from config.logging import logger
from .Read_stream_data import raw_stream_df
from .transform_data import transform_weather_data
from .write_database import write_to_database
import traceback


def main():

    try:
        # =========================================================
        # 1. BRONZE LAYER
        # =========================================================

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

        logger.info("Bronze streaming started successfully.")

        # =========================================================
        # 2. TRANSFORM DATA
        # =========================================================

        transformed_df = transform_weather_data(bronze_df)

        # =========================================================
        # 3. SILVER LAYER
        # =========================================================

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

        logger.info("Silver streaming started successfully.")

        # =========================================================
        # 4. POSTGRESQL / GOLD LAYER
        # =========================================================

        write_query = (
            transformed_df.writeStream
            .foreachBatch(write_to_database)
            .option(
                "checkpointLocation",
                "file:///C:/Users/HP/OneDrive/Desktop/weather/checkpoint_database"
            )
            .start()
        )

        logger.info("PostgreSQL streaming started successfully.")
        spark.streams.awaitAnyTermination()

    except Exception as e:
        logger.error(f"Error occured {e}")
        logger.error(traceback.format_exc())
        raise
    

if __name__ == "__main__":
    main()
    
