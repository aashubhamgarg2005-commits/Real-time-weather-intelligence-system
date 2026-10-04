
-- ============================================
-- WEATHER DATABASE TABLES
-- ============================================

-----------------------------------------------
-- 1. STAGING DIM TABLE 
-----------------------------------------------

CREATE TABLE IF NOT EXISTS staging_dim_location (
    location_id BIGINT,
    district VARCHAR(100),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timezone VARCHAR(100)
);

--------------------------------------------------
-- 2. STAGING FACT TABLE
--------------------------------------------------
CREATE TABLE IF NOT EXISTS staging_fact_weather (
    weather_id BIGINT,
    location_id BIGINT,
    time TIMESTAMP,
    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    apparent_temperature DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    rain DOUBLE PRECISION,
    showers DOUBLE PRECISION,
    snowfall DOUBLE PRECISION,
    cloud_cover DOUBLE PRECISION,
    pressure_msl DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION,
    wind_direction_10m DOUBLE PRECISION,
    wind_gusts_10m DOUBLE PRECISION
);

-- --------------------------------------------
-- 1. DIM LOCATION
-- --------------------------------------------

CREATE TABLE IF NOT EXISTS dim_location (
    location_id BIGINT PRIMARY KEY,
    district VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    timezone VARCHAR(100)
);


-- --------------------------------------------
-- 2. FACT WEATHER
-- --------------------------------------------

CREATE TABLE IF NOT EXISTS fact_weather (
    weather_id BIGINT PRIMARY KEY,
    location_id BIGINT NOT NULL,
    time TIMESTAMP NOT NULL,

    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    apparent_temperature DOUBLE PRECISION,

    precipitation DOUBLE PRECISION,
    rain DOUBLE PRECISION,
    showers DOUBLE PRECISION,
    snowfall DOUBLE PRECISION,

    cloud_cover DOUBLE PRECISION,
    pressure_msl DOUBLE PRECISION,

    wind_speed_10m DOUBLE PRECISION,
    wind_direction_10m DOUBLE PRECISION,
    wind_gusts_10m DOUBLE PRECISION,

    CONSTRAINT fk_fact_weather_location
        FOREIGN KEY (location_id)
        REFERENCES dim_location(location_id)
);


-- --------------------------------------------
-- INDEXES
-- --------------------------------------------

CREATE INDEX IF NOT EXISTS idx_fact_weather_location
ON fact_weather(location_id);

CREATE INDEX IF NOT EXISTS idx_fact_weather_time
ON fact_weather(time);

CREATE INDEX IF NOT EXISTS idx_dim_location_district
ON dim_location(district);
