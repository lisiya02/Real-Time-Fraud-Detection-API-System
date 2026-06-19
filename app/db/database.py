from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# The engine manages the actual connection pool to PostgreSQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal is a factory that creates new database session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class all our ORM models will inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI routes.
    Yields a database session and guarantees it's closed afterward,
    even if an error occurs during the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()