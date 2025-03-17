import logging
from aiogram import Router
from filters.middleware_filteers import MyTrueFilter
from lexicon.middleware_lexicon import LEXICON_RU

from aiogram.types import Message
logger = logging.getLogger(__name__)


router = Router()



@router.message(MyTrueFilter())
async def send_echo(message: Message):
    logger.debug('Вошли в эхо-хэндлер')
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])
