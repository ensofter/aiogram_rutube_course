import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config, Config
from handlers import middleware_other_router, middleware_user_router

from middleware.inner import FirstInnerMiddleware, SecondInnerMiddleware, ThirdInnerMiddleware
from middleware.outer import FirstOuterMiddleware, SecondOuterMiddleware, ThirdOuterMiddleware

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d '
                                                '%(name)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    conf: Config = load_config()

    bot = Bot(token=conf.tg_bot.bot_token)
    dp = Dispatcher()

    dp.include_routers(middleware_user_router.router)
    dp.include_routers(middleware_other_router.router)

    # регистрация мидлварей
    dp.update.outer_middleware(FirstOuterMiddleware())
    middleware_user_router.router.callback_query.outer_middleware(SecondOuterMiddleware())
    middleware_other_router.router.message.outer_middleware(ThirdOuterMiddleware())
    middleware_user_router.router.message.middleware(FirstInnerMiddleware())
    middleware_user_router.router.message.middleware(SecondInnerMiddleware())
    middleware_other_router.router.message.middleware(ThirdInnerMiddleware())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
