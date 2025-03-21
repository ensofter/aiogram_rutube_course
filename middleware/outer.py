import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


logger = logging.getLogger(__name__)


class FirstOuterMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        logger.debug(
            f'Вошли в миддлвари {__class__.__name__}, тип события {event.__class__.__name__}',
        )
        logger.debug(
            f'!!! Это handler: {handler}'
        )
        logger.debug(
            f'!!! это event: {event.model_dump_json(indent=4, exclude_none=True)}'
        )

        logger.debug(
            f'!!! это data: {data}'
        )

        result = await handler(event, data)

        logger.debug(f'Выходим из миддлвари {__class__.__name__}')

        return result


class SecondOuterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logger.debug(
            'Вошли в миддлвари %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        result = await handler(event, data)

        logger.debug('Выходим из миддлвари %s', __class__.__name__)

        return result

class ThirdOuterMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        result = await handler(event, data)

        logger.debug('Выходим из миддлвари %s', __class__.__name__)


        return result