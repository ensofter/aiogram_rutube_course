import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)
        self.session_maker = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
