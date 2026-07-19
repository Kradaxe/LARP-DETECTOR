import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Use SQLite for local development unless DATABASE_URL is explicitly set to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
    DATABASE_URL = "sqlite:///./larp_detector.db"

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
