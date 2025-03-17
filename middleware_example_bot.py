from environs import Env
import logging
from aiogram import Bot, Dispatcher
import asyncio

from config.config import load_config, Config
from handlers import middleware_other_router

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d '
                                                '%(name)s - %(message)s')
logger = logging.getLogger(__name__)



async def main():
    conf: Config = load_config()

    bot = Bot(token=conf.tg_bot.bot_token)
    dp = Dispatcher()

    dp.include_routers(middleware_other_router.router)
    dp.include_routers(middleware_user_router.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())