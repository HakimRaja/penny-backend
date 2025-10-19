from sqlalchemy import create_engine,text
from core.config import settings

engine = create_engine(settings.DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("Select version();"))
            print("Connected to database successfully!")
            print("PostgreSQL version:", result.scalar())
    except Exception as e:
        print("DB connection failed!")
        print(e)