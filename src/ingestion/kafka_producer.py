from kafka import KafkaProducer
from config.config import kafka_broker_url
from config.logging import logger

def create_kafka_producer():
    """
    Creates a Kafka producer instance.

    Returns:
        KafkaProducer: An instance of KafkaProducer.
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_broker_url,
            value_serializer=lambda v: str(v).encode('utf-8')  # Serialize the message to bytes
        )
        logger.info("Kafka producer created successfully.")
        return producer
    except Exception as e:
        logger.error(f"Error creating Kafka producer: {e}")
        return None