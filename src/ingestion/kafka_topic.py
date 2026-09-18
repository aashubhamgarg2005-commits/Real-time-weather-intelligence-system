from confluent_kafka.admin import AdminClient, NewTopic
from config.config import kafka_broker_url, kafka_topic
from config.logging import logger
def create_kafka_topic():
    """
    Creates a Kafka topic if it does not already exist.

    Returns:
        None
    """
    try:
        metadata = AdminClient({'bootstrap.servers': kafka_broker_url}).list_topics(timeout=10)
        if kafka_topic in metadata.topics:
            logger.info(f"Kafka topic '{kafka_topic}' already exists.")
            return
        admin_client = AdminClient({'bootstrap.servers': kafka_broker_url})
        topic = NewTopic(kafka_topic, num_partitions=1, replication_factor=1)
        admin_client.create_topics([topic])
        logger.info(f"Kafka topic '{kafka_topic}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating Kafka topic '{kafka_topic}': {e}")
