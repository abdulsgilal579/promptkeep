import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://promptkeep:promptkeep@localhost:5432/promptkeep",
)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    # Import models so they're registered with Base before create_all
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)