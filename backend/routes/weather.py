from fastapi import APIRouter, HTTPException
from psycopg2.extras import RealDictCursor

from backend.database import get_connection


router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"]
)


@router.get("/latest")
def get_latest_weather():

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        query = """
            SELECT
                d.location_id,
                d.district,
                d.latitude,
                d.longitude,
                d.timezone,

                f.weather_id,
                f.time,
                f.temperature_2m,
                f.relative_humidity_2m,
                f.apparent_temperature,
                f.precipitation,
                f.rain,
                f.showers,
                f.snowfall,
                f.cloud_cover,
                f.pressure_msl,
                f.wind_speed_10m,
                f.wind_direction_10m,
                f.wind_gusts_10m

            FROM dim_location d

            JOIN LATERAL (
                SELECT *
                FROM fact_weather f
                WHERE f.location_id = d.location_id
                ORDER BY f.time DESC
                LIMIT 1
            ) f ON TRUE

            ORDER BY d.district;
        """

        cursor.execute(query)

        data = cursor.fetchall()

        return {
            "count": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@router.get("/{district}")
def get_weather_by_district(district: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        query = """
            SELECT
                d.location_id,
                d.district,
                d.latitude,
                d.longitude,
                d.timezone,

                f.weather_id,
                f.time,
                f.temperature_2m,
                f.relative_humidity_2m,
                f.apparent_temperature,
                f.precipitation,
                f.rain,
                f.showers,
                f.snowfall,
                f.cloud_cover,
                f.pressure_msl,
                f.wind_speed_10m,
                f.wind_direction_10m,
                f.wind_gusts_10m

            FROM dim_location d

            JOIN LATERAL (
                SELECT *
                FROM fact_weather f
                WHERE f.location_id = d.location_id
                ORDER BY f.time DESC
                LIMIT 1
            ) f ON TRUE

            WHERE LOWER(d.district) = LOWER(%s);
        """

        cursor.execute(query, (district,))

        data = cursor.fetchone()

        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No weather data found for {district}"
            )

        return data

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()