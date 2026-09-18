import os
import dotenv

dotenv.load_dotenv()

weather_api_url = os.getenv("WEATHER_API_URL")
kafka_broker_url = os.getenv("KAFKA_BROKER_URL")
kafka_topic = os.getenv("KAFKA_TOPIC_NAME")
minio_endpoint = os.getenv("MINIO_ENDPOINT")
minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")
minio_bucket_name = os.getenv("MINIO_BUCKET_NAME")
minio_secure = os.getenv("MINIO_SECURE")