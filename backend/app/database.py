from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings

# 1. Configure SQLite-specific arguments
# check_same_thread=False is required for SQLite to work with FastAPI's concurrency
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# 2. Create the engine with the proper arguments
engine = create_engine(
    settings.database_url, 
    future=True, 
    connect_args=connect_args
)

# 3. Create the Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 4. Modern SQLAlchemy 2.0 Base class
class Base(DeclarativeBase):
    pass

# 5. Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()