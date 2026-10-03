from pyspark.sql.types import *

weather_schema = StructType([
    StructField("district",StringType(),True),
    StructField("latitude",DoubleType(),True),
    StructField("longitude",DoubleType(),True),
    StructField("weather",StructType([
        StructField("timezone",StringType(),True),
        StructField("current",StructType([
            StructField("time",StringType(),True),
            StructField("temperature_2m",DoubleType(),True),
            StructField("relative_humidity_2m",DoubleType(),True),
            StructField("apparent_temperature",DoubleType(),True),
            StructField("precipitation",DoubleType(),True),
            StructField("rain",DoubleType(),True),
            StructField("showers",DoubleType(),True),
            StructField("snowfall",DoubleType(),True),
            StructField("cloud_cover",DoubleType(),True),
            StructField("pressure_msl",DoubleType(),True),
            StructField("wind_speed_10m",DoubleType(),True),
            StructField("wind_direction_10m",DoubleType(),True),
            StructField("wind_gusts_10m",DoubleType(),True)
        ]),True)  
    ]),True),
    
])