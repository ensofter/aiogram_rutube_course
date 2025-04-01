from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Dict, Any, Callable, Awaitable
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbMiddleWare(BaseMiddleware):
    def __init__(self):
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)
