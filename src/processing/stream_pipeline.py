from .spark_session import spark
from config.logging import logger
from .Read_stream_data import raw_stream_df
from .print_data import print_stream_data
import traceback
from src.storage.create_minio_bucket import MinioBucketManager
from datetime import datetime


def main():
    """
    Main function to process streaming data from Kafka
    and store it in MinIO.
    """

    try:
        # Initialize MinIO bucket manager
        minio_manager = MinioBucketManager()

        if not minio_manager.create_bucket():
            logger.error("Failed to create or access MinIO bucket. Exiting.")
            return

        # Date-based output path
        current_date = datetime.now().strftime("%Y-%m-%d")

        output_path = (
            f"s3a://{minio_manager.bucket_name}"
            f"/raw_weather_data/{current_date}/"
        )

        # Checkpoint stored in MinIO
        checkpoint_path = (
            f"s3a://{minio_manager.bucket_name}"
            "/checkpoints/weather_data/"
        )

        logger.info(f"Output path: {output_path}")
        logger.info(f"Checkpoint path: {checkpoint_path}")
        

        query = (
            raw_stream_df.writeStream
            .format("json")
            .outputMode("append")
            .option("path", output_path)
            .option("checkpointLocation", checkpoint_path)
            .start()
        )

        logger.info("Streaming query started successfully.")

        query.awaitTermination()

        print_stream_data()

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()