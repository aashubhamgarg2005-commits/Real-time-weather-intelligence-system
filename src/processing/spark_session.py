from pyspark.sql import SparkSession


KAFKA_CONNECTOR_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.spark"
    r"\spark-sql-kafka-0-10_2.13\jars"
    r"\spark-sql-kafka-0-10_2.13-4.2.0.jar"
)

KAFKA_TOKEN_PROVIDER_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.spark"
    r"\spark-token-provider-kafka-0-10_2.13\jars"
    r"\spark-token-provider-kafka-0-10_2.13-4.2.0.jar"
)

KAFKA_CLIENTS_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.kafka"
    r"\kafka-clients\jars"
    r"\kafka-clients-3.9.2.jar"
)

COMMONS_POOL_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.commons"
    r"\commons-pool2\jars"
    r"\commons-pool2-2.13.1.jar"
)


spark = (
    SparkSession.builder
    .appName("Real-Time Weather Streaming")
    .master("local[2]")

    .config(
        "spark.jars",
        ",".join([
            KAFKA_CONNECTOR_JAR,
            KAFKA_TOKEN_PROVIDER_JAR,
            KAFKA_CLIENTS_JAR,
            COMMONS_POOL_JAR
        ])
    )

    .config(
        "spark.driver.extraJavaOptions",
        "-Djava.library.path=C:/hadoop/bin"
    )

    .config(
        "spark.executor.extraJavaOptions",
        "-Djava.library.path=C:/hadoop/bin"
    )

    .config("spark.hadoop.native.lib", "true")
    .config("spark.hadoop.io.native.lib.available", "true")
    .config("spark.hadoop.home.dir", r"C:\hadoop")
    .config("spark.hadoop.native.lib.path", r"C:\hadoop\bin")

    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")