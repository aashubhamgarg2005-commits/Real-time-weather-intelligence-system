
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.weather import router as weather_router


app = FastAPI(
    title="Weather API",
    description="Live Weather Data API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Routes
# =========================================================

app.include_router(weather_router)


# =========================================================
# Health
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Weather API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
