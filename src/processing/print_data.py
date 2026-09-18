from pyspark.sql.functions import col
from .Read_stream_data import raw_stream_df

def print_stream_data():
    """
    Function to print the streaming data from Kafka to the console.
    """
    display_df = raw_stream_df.select(
        col("key").cast("string").alias("key"),
        col("value").cast("string").alias("value"),
        col("topic"),
        col("partition"),
        col("offset"),
        col("timestamp")
    )

    print("Starting Spark Kafka consumer...")

    query = (
        display_df.writeStream
        .format("console")
        .outputMode("append")
        .option("truncate", False)
        .option("numRows", 5)
        .option(
            "checkpointLocation",
            "s3a://weather-data/checkpoints/spark_console_test/"
        )
        .start()
    )

    print("Spark streaming query started.")
    query.awaitTermination()
display_df = raw_stream_df.select(
    col("key").cast("string").alias("key"),
    col("value").cast("string").alias("value"),
    col("topic"),
    col("partition"),
    col("offset"),
    col("timestamp")
)

print("Starting Spark Kafka consumer...")

query = (
    display_df.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .option("numRows", 5)
    .option(
        "checkpointLocation",
        "s3a://weather-data/checkpoints/spark_console_test/"
    )
    .start()
)

print("Spark streaming query started.")
query.awaitTermination()