import asyncio
import logging

from aiogram import Bot, Dispatcher
from environs import Env

from handlers import handler


env = Env()
env.read_env()

token = env('BOT_TOKEN')

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s #%(levelname)-8s %(filename)s:%(lineno)d '
                                                    '%(name)s - %(message)s')
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(handler.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
