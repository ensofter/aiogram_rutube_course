import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery

from filters.middleware_filteers import MyTrueFilter, MyFalseFilter
from lexicon.middleware_lexicon import LEXICON_RU

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart(), MyTrueFilter())
async def handle_cmd_start(message: Message):
    logger.debug('Вошли в хэндлер, обрабатывающий команду start')

    button = InlineKeyboardButton(
        text='Кнопка',
        callback_data='button_pressed'
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(text=LEXICON_RU['/start'], reply_markup=markup)
    logger.debug('Выходим из хэндлера, обрабатывающего команду /start')


@router.callback_query(F.data, MyTrueFilter())
async def handle_clbck_button_pressed(callback: CallbackQuery):
    logger.debug('Вошли в хэндлер, обрабатывающий нажатие на инлайн-кнопку')
    await callback.answer(text=LEXICON_RU['button_pressed'])
    logger.debug('Выходим из хэндлера, обрабатывающего нажатие на инлайн-кнопку')


@router.message(F.text, MyFalseFilter())
async def handle_every_message(message: Message):
    logger.debug('Вошли в хэндлер, обрабатывающий любой текст')
    logger.debug('Выходим из хэндлера, обрабатывающего лоюбой текст')
