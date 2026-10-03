@echo off
setlocal

title Weather Data Pipeline

echo.
echo ==========================================
echo       WEATHER DATA PIPELINE
echo ==========================================
echo.

REM ==================================================
REM PATH CONFIGURATION
REM ==================================================

set "PROJECT_DIR=C:\Users\HP\OneDrive\Desktop\weather"
set "KAFKA_DIR=C:\kafka"


REM ==================================================
REM 1. START KAFKA
REM ==================================================

echo [1/3] Starting Kafka...
echo.

start "Kafka Server" cmd /k "cd /d %KAFKA_DIR% && bin\windows\kafka-server-start.bat config\server.properties"

echo Waiting for Kafka to start...
timeout /t 10 /nobreak >nul

echo Kafka started.
echo.


REM ==================================================
REM 2. START WEATHER PRODUCER
REM ==================================================

echo [2/3] Starting Weather Kafka Producer...
echo.

start "Weather Producer" cmd /k "cd /d %PROJECT_DIR% && call venv\Scripts\activate && python -m src.ingestion.produce_data"

echo Weather Producer started.
echo.


REM ==================================================
REM WAIT BEFORE STARTING SPARK
REM ==================================================

echo Waiting 10 seconds before starting Spark Streaming...
timeout /t 10 /nobreak >nul

REM ==================================================
REM 3. START SPARK STREAMING
REM ==================================================

echo [3/3] Starting Spark Streaming Pipeline...
echo.

start "Spark Streaming" cmd /k "cd /d %PROJECT_DIR% && call venv\Scripts\activate && python -m src.processing.stream_pipeline"

echo Spark Streaming started.
echo.


REM ==================================================
REM PIPELINE INFORMATION
REM ==================================================

echo ==========================================
echo       PIPELINE STARTED SUCCESSFULLY
echo ==========================================
echo.

echo Kafka:
echo   Broker  : localhost:9092
echo.

echo Kafka Topic:
echo   weather-data
echo.

echo Services:
echo   1. Kafka
echo   2. Weather Producer
echo   3. Spark Streaming
echo.

echo ==========================================

pause