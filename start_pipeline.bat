```bat
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
set "MINIO_EXE=C:\Users\HP\Downloads\minio.windows-amd64.RELEASE.2025-09-07T16-13-09Z.exe"
set "MINIO_DATA=C:\minio-data"

REM ==================================================
REM 1. START KAFKA
REM ==================================================

echo [1/4] Starting Kafka...
echo.

start "Kafka Server" cmd /k "cd /d %KAFKA_DIR% && bin\windows\kafka-server-start.bat config\server.properties"

echo Waiting for Kafka to start...
timeout /t 10 /nobreak >nul

echo Kafka started.
echo.

REM ==================================================
REM 2. START MINIO
REM ==================================================

echo [2/4] Starting MinIO...
echo.

start "MinIO Server" cmd /k "%MINIO_EXE% server %MINIO_DATA% --console-address :9001"

echo Waiting for MinIO to start...
timeout /t 5 /nobreak >nul

echo MinIO started.
echo.

REM ==================================================
REM 3. START WEATHER PRODUCER
REM ==================================================

echo [3/4] Starting Weather Kafka Producer...
echo.

start "Weather Producer" cmd /k "cd /d %PROJECT_DIR% && call venv\Scripts\activate && python -m src.ingestion.produce_data"

echo Weather Producer started.
echo.

REM Wait 20 seconds before starting Spark
echo Waiting 20 seconds before starting Spark Streaming...
timeout /t 20 /nobreak >nul

REM ==================================================
REM 4. START SPARK STREAMING
REM ==================================================

echo [4/4] Starting Spark Streaming Pipeline...
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
echo MinIO:
echo   API     : localhost:9000
echo   Console : localhost:9001
echo.
echo Kafka Topic:
echo   weather-data
echo.
echo Services:
echo   1. Kafka
echo   2. MinIO
echo   3. Weather Producer
echo   4. Spark Streaming
echo.
echo ==========================================

pause
```
