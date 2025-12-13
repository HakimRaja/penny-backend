# src/database/connection.py

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from src.config.settings import settings

# 1. Database URL (must be async)
# Example: postgresql+asyncpg://user:pass@localhost:5432/dbname
DATABASE_URL = str(settings.DATABASE_URL)

# 2. Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# 3. Async session maker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Dependency for FastAPI
async def get_db_session():
    async with async_session_maker() as session:
        yield session


# 5. Test database connection
async def test_connection():
    print("🔬 Attempting database connection test...")
    try:
        async with async_session_maker() as session:
            await session.exec(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection FAILED!")
        print(f"Error: {e}")
        raise e


# 6. Create all tables (async version)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
