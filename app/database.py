from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# AlloyDB connection string
DB_URL = os.getenv("DB_URL", "postgresql://postgres:<PASS>@34.41.66.108:5432/postgres")

engine = create_engine(DB_URL, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
