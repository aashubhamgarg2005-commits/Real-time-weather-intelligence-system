from .spark_session import spark
from config.config import kafka_topic,kafka_broker_url
from config.logging import logger
from pyspark.sql.functions import col

raw_stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker_url) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "latest") \
    .load()

print("Raw stream DataFrame schema:")
raw_stream_df.printSchema()

