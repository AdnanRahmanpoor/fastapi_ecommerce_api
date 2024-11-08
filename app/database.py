'''
Config Database for the project
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')

# Define Base model
Base = declarative_base()


engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# initiate database and create models (asynchronous)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)