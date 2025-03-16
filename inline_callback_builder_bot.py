from aiogram import Bot, Dispatcher
import logging
import asyncio
from environs import Env
from handlers.handlers_for_cllbackbuilder import router


conf = Env()
conf.read_env()

token = conf('BOT_TOKEN')

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(levelname)-8s %(filename)s:%(lineno)s'
                                                    '%(name)s - %(message)s')


    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
