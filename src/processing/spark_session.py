from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[2]")
    .appName("Real-time Weather Data")

    # =========================
    # Driver
    # =========================
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.blockManager.port", "0")

    # =========================
    # Network
    # =========================
    .config("spark.network.timeout", "120s")
    .config("spark.executor.heartbeatInterval", "20s")

    # =========================
    # Kafka + Hadoop AWS
    # =========================
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0,"
        "org.apache.hadoop:hadoop-aws:3.4.1"
    )

    # =========================
    # MinIO
    # =========================
    .config(
        "spark.hadoop.fs.s3a.endpoint",
        "http://127.0.0.1:9000"
    )

    .config(
        "spark.hadoop.fs.s3a.access.key",
        "minioadmin"
    )

    .config(
        "spark.hadoop.fs.s3a.secret.key",
        "minioadmin"
    )

    .config(
        "spark.hadoop.fs.s3a.path.style.access",
        "true"
    )

    .config(
        "spark.hadoop.fs.s3a.connection.ssl.enabled",
        "false"
    )

    .config(
        "spark.hadoop.fs.s3a.impl",
        "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )

    # =========================
    # IMPORTANT:
    # Avoid Windows NativeIO
    # =========================
    .config(
        "spark.hadoop.io.native.lib.available",
        "false"
    )

    # In-memory S3A buffering
    .config(
        "spark.hadoop.fs.s3a.fast.upload",
        "true"
    )

    .config(
        "spark.hadoop.fs.s3a.fast.upload.buffer",
        "bytebuffer"
    )

    .config(
        "spark.hadoop.fs.s3a.fast.upload.active.blocks",
        "2"
    )

    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")