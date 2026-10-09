# Real-Time Weather Intelligence System

A real-time weather data pipeline that ingests live weather observations for multiple cities and districts, streams them through Kafka and Apache Spark, enriches the data, stores it in PostgreSQL for analytics, and exposes it through a FastAPI backend and interactive dashboard.

## Overview

This project is designed for streaming, processing, and serving weather intelligence in near real time. It continuously fetches weather data from a public weather API, publishes it to Kafka, processes it with Spark Structured Streaming, writes curated results into a PostgreSQL warehouse, and exposes the latest data through a REST API and browser-based dashboard.

The system follows a modern data-engineering pattern:

- Ingestion layer: real-time weather fetcher + Kafka messaging
- Processing layer: Spark Streaming transformation and validation
- Storage layer: PostgreSQL dimensional and fact tables
- Serving layer: FastAPI REST API and frontend dashboard

## Architecture

```text
Weather API (Open-Meteo / live source)
                |
                v
        fetch_data.py
                |
                v
      Kafka Producer / Topic
                |
                v
      Spark Structured Streaming
      (Bronze -> Transform -> Silver)
                |
                v
       PostgreSQL Warehouse
       dim_location + fact_weather
                |
                v
      FastAPI REST API
                |
                v
   Static Frontend Dashboard
```

## Key Features

- Live weather ingestion for multiple districts
- Kafka-based message streaming pipeline
- Spark Structured Streaming transformation and processing
- Bronze/Silver-style streaming workflow with checkpoints
- PostgreSQL warehouse model for location and weather fact data
- FastAPI backend with district and latest-weather endpoints
- Lightweight frontend dashboard for observing current and recent conditions
- Support for periodic re-fetching and real-time updates

## Tech Stack

- Python
- Kafka
- Apache Spark
- PostgreSQL
- FastAPI
- JavaScript / HTML / CSS
- Requests and dotenv

## Project Structure

```text
weather/
├── backend/
│   ├── database.py
│   ├── main.py
│   └── routes/
│       └── weather.py
├── config/
│   ├── config.py
│   ├── location.py
│   └── logging.py
├── data/
├── dags/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── src/
│   ├── database/
│   │   ├── database.sql
│   │   └── postgres.py
│   ├── ingestion/
│   │   ├── fetch_data.py
│   │   ├── kafka_producer.py
│   │   ├── kafka_topic.py
│   │   ├── produce_data.py
│   │   └── ...
│   └── processing/
│       ├── Read_stream_data.py
│       ├── prepare_gold_data.py
│       ├── spark_session.py
│       ├── stream_pipeline.py
│       ├── transform_data.py
│       ├── weather_schema.py
│       └── write_database.py
├── tests/
├── .env
├── requirements.txt
├── start_pipeline.bat
├── README.md
└── .gitignore
```

## Prerequisites

Before running the project, ensure the following are installed and available:

- Python 3.9+
- Apache Kafka
- Apache Spark
- PostgreSQL
- Git
- Access to a weather API source configured in environment variables

## Environment Configuration

Create a `.env` file in the project root with the required configuration values.

Example structure:

```env
WEATHER_API_URL=your_weather_api_url
KAFKA_BROKER_URL=localhost:9092
KAFKA_TOPIC_NAME=weather-data
MINIO_ENDPOINT=your_minio_endpoint
MINIO_ACCESS_KEY=your_minio_access_key
MINIO_SECRET_KEY=your_minio_secret_key
MINIO_BUCKET_NAME=your_bucket
MINIO_SECURE=false
JDBC_URL=jdbc:postgresql://localhost:5432/weather_db
JDBC_USER=postgres
JDBC_PASSWORD=your_password
JDBC_DRIVER=org.postgresql.Driver
```

Notes:

- Update the values to match your local or cloud environment.
- Kafka must be running before starting the producer pipeline.
- PostgreSQL must already exist and the warehouse schema should be initialized.

## Database Setup

Initialize the weather warehouse using the schema defined in `src/database/database.sql`.

```sql
-- Example: create schema and tables
-- Execute the SQL script in PostgreSQL
```

The script creates:

- `staging_dim_location`
- `staging_fact_weather`
- `dim_location`
- `fact_weather`
- supporting indexes for operational querying

## Installation

Clone the repository and install the required Python dependencies:

```bash
git clone <repository-url>
cd weather
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Pipeline

### 1. Start Kafka

Make sure Kafka is running on the configured broker address.

### 2. Start the weather producer

```bash
python -m src.ingestion.produce_data
```

This module fetches weather data periodically and publishes each record to the Kafka topic.

### 3. Start the Spark streaming pipeline

```bash
python -m src.processing.stream_pipeline
```

This component reads Kafka messages, transforms the JSON payload into the expected weather schema, writes intermediate data to the Bronze/Silver directories, and pushes the results to PostgreSQL.

### 4. Start the FastAPI backend

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Open the frontend dashboard

Open `frontend/index.html` in the browser or serve the frontend through a local web server if needed.

### Windows helper

This project includes a helper script:

```bash
start_pipeline.bat
```

It starts Kafka, the producer, and the Spark streaming job in one command sequence.

## API Endpoints

The backend exposes weather endpoints through FastAPI.

### Latest weather across all districts

```http
GET /api/weather/latest
```

Returns the latest available weather reading for each district.

### Weather by district

```http
GET /api/weather/{district}
```

Example:

```http
GET /api/weather/meerut
```

Custom health and service checks are also exposed via:

```http
GET /
GET /health
```

## Data Flow

1. Fetch weather data for configured districts
2. Serialize the payload and publish it to Kafka
3. Read Kafka messages in Spark Structured Streaming
4. Transform raw JSON into schema-based aggregated weather records
5. Store transformed results in PostgreSQL fact and dimension tables
6. Query latest weather using FastAPI
7. Render data in the frontend dashboard

## Dashboard

The frontend dashboard provides a clean interface to:

- select a district
- view current temperature and conditions
- inspect humidity, wind, pressure, and rainfall
- track recent observations and alerts

## Notes

- The project is optimized for in-house or local environment deployment.
- Some services such as Kafka and Spark require external setup and correct local paths.
- Checkpoint directories are part of the pipeline state and should be maintained if the stream restarts.

## Future Enhancements

- Add Docker containerization for easier deployment
- Add historical analytics and trend visualization
- Extend to multiple regions and weather providers
- Add authentication and role-based access for admin endpoints
- Introduce monitoring, alerts, and automated dashboards

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors

This project is suitable for learning, prototyping, and demonstration of a real-time data engineering pipeline.
