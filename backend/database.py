# backend/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not found in .env file")
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
    return engine

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            return bool(result == 1)
    except SQLAlchemyError as e:
        print("Database connection failed:", e)
        return False
