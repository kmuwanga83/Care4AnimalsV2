from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers.health import router as health_router
from .routers.content import router as content_router
from .routers.sms import router as sms_router
from .routers.analytics import router as analytics_router
from .routers.lessons import router as lessons_router
from .api import analytics, lessons
from .database import engine
from . import models

# 1. Initialize the ONLY FastAPI instance
app = FastAPI(
    title=settings.app_name,
    version="2.0.0"
)

# 2. Ensure Database Tables are created
models.Base.metadata.create_all(bind=engine)

# 3. Configure CORS for the React Dashboard
origins = [
    settings.frontend_url,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Register Routers to the app
# Health check
app.include_router(health_router)

# Content & SMS
app.include_router(content_router)
app.include_router(sms_router)

# Analytics (The path for your Dashboard UI)
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

# Lessons (The path for your Seeding Script)
# This registers the POST /lessons/ endpoint from routers/lessons.py
app.include_router(lessons_router)

# Optional: Versioned API path for lessons
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["lessons"])

# 5. Root Endpoint with institutional branding
@app.get("/")
async def root():
    return {
        "message": "Care4Animals API is live",
        "version": "2.0.0",
        "partners": ["Bugema University", "WTS Foundation"]
    }