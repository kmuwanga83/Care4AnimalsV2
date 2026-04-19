from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers.health import router as health_router
from .routers.content import router as content_router
from .routers.sms import router as sms_router
from .routers.analytics import router as analytics_router
from .routers.lessons import router as lessons_router
from .database import engine
from . import models

# This line ensures tables are created automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app = FastAPI(title=settings.app_name)

# Professional CORS implementation
# This allows your React dashboard to securely fetch data
origins = [
    settings.frontend_url,      # e.g., https://care4animals-ui.vercel.app
    "http://localhost:5173",    # Local Vite dev server
    "http://127.0.0.1:5173",    # Local loopback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],        # Allows GET, POST, etc.
    allow_headers=["*"],
)

# Route Registration
app.include_router(health_router)
app.include_router(content_router)
app.include_router(sms_router)
app.include_router(analytics_router)
app.include_router(lessons_router)

@app.get("/")
async def root():
    return {
        "message": "Care4Animals API is live",
        "version": "2.0.0",
        "partners": ["Bugema University", "WTS Foundation"]
    }