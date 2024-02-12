from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import DB_HOST, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
"postgresql+psycopg2://postgres:postgres@db:5432/postgres"
# "postgresql://postgres:postgres@localhost:5432/merchandising"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
