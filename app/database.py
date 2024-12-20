from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_SYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
