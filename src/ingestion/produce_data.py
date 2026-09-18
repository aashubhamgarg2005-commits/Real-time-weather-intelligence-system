
from .fetch_data import fetch_weather_data
from .kafka_producer import create_kafka_producer
from .kafka_topic import create_kafka_topic

from config.config import kafka_topic
from config.logging import logger


def produce_weather_data():
    """
    Fetches weather data and produces it to a Kafka topic.
    """

    producer = None

    try:
        # Create Kafka topic if it doesn't exist
        create_kafka_topic()

        # Create Kafka producer
        producer = create_kafka_producer()

        if producer is None:
            logger.error("Kafka producer creation failed. Exiting.")
            return

        # fetch_weather_data() is already a continuous generator
        for weather_data in fetch_weather_data():

            try:
                # Make sure we received a dictionary
                if not isinstance(weather_data, dict):
                    logger.warning(
                        "Received invalid weather data format. Skipping."
                    )
                    continue

                # Send weather data to Kafka
                future = producer.send(
                    kafka_topic,
                    value=weather_data
                )

                # Wait for Kafka acknowledgement
                record_metadata = future.get(timeout=10)

                logger.info(
                    f"Produced weather data for "
                    f"{weather_data['district']} to Kafka | "
                    f"topic={record_metadata.topic} | "
                    f"partition={record_metadata.partition} | "
                    f"offset={record_metadata.offset}"
                )

                logger.info(
                    f"Weather data for "
                    f"{weather_data['district']} "
                    f"produced to Kafka successfully."
                )

            except Exception as e:
                logger.error(
                    f"Error producing weather data: {e}"
                )

    except Exception as e:
        logger.error(
            f"Error in produce_weather_data: {e}"
        )

    finally:
        if producer is not None:
            producer.flush()
            producer.close()


if __name__ == "__main__":
    produce_weather_data()
