from app.db.database import Base, engine
from app.db import models  # noqa: F401 - import ensures models are registered with Base


def init_db():
    """Create all tables defined in models.py if they don't already exist."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()