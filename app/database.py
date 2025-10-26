import os
import asyncio
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text


# Load environment variables from .env
load_dotenv()

# Create declarative base for SQLAlchemy models
Base = declarative_base()

# Build DATABASE_URL from environment or use full URL if provided
DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Initialize async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Check that the connection to PostgreSQL works correctly.
async def init_db(retries: int = 5, delay: int = 3) -> None:
    """
    Initialize and test PostgreSQL connection at app startup.
    Retries several times if the connection fails.
    """
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                print(
                    "\033[92m✅ PostgreSQL connection successfully established!\033[0m"
                )
                return
        except Exception as e:
            print(
                f"\033[93m Attempt {attempt}/{retries} failed to connect to PostgreSQL:\033[0m",
                e,
            )
            if attempt < retries:
                print(f"🔁 Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print(
                    "\033[91m Could not connect to PostgreSQL after multiple attempts.\033[0m"
                )
                raise e


# Provides an async context manager for database sessions
# Allows using "async with" to open and automatically close the session

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
