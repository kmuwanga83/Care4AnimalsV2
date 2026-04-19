from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers.health import router as health_router
from .routers.content import router as content_router
from .routers.sms import router as sms_router
from .routers import analytics

app = FastAPI(title=settings.app_name)

# Professional CORS implementation
origins = [
    settings.frontend_url,      # From your .env (e.g., http://localhost:5173)
    "http://localhost:5173",    # Local Vite dev server
    "http://127.0.0.1:5173",    # Local loopback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(content_router)
app.include_router(sms_router)
app.include_router(analytics.router)