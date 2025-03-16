import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command
from environs import Env
from keyboards.inline_keyboard import create_inline_kb

logger = logging.getLogger(__name__)

conf = Env()
conf.read_env()
token = conf('BOT_TOKEN')
admin = conf('ADMIN_ID')


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d'
                                                    '%(name)s - %(message)s')

    bot = Bot(token)
    dp = Dispatcher()

    group_name = 'aiogram_stepik_course'
    url_button_0 = InlineKeyboardButton(
        text='Группа "Телеграм-боты на AIOgram"',
        url=f'tg://resolve?domain={group_name}'
    )
    url_button_1 = InlineKeyboardButton(
        text='Курс телеграмм боты на python и aiogram',
        url='https://stepik.org/120924'
    )
    url_button_2 = InlineKeyboardButton(
        text='Документации Telegram Bot API',
        url='https://core.telegram.org/bots/api'
    )
    url_button_3 = InlineKeyboardButton(
        text='Автор курса на Степике по телеграм-ботам',
        url=f'tg://user?id={admin}'
    )

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [url_button_1, url_button_0],
            [url_button_2, url_button_3]
        ]
    )

    big_button_1 = InlineKeyboardButton(
        text='БОЛЬШАЯ КНОПКА 1',
        callback_data='big_button_1_called'
    )
    big_button_2 = InlineKeyboardButton(
        text='БОЛЬШАЯ КНОПКА 2',
        callback_data='big_button_2_pressed'
    )

    callback_inline_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [big_button_1],
            [big_button_2]
        ]
    )


    @dp.message(CommandStart())
    async def handle_cmd_start(message: Message):
        await message.answer(text='Это две кнопки с callback', reply_markup=callback_inline_button)

    @dp.message(Command('help'))
    async def handle_cmd_help(message: Message):
        logger.info('!!!')
        await message.answer(text='Это инлайн билдер клавиатуры', reply_markup=create_inline_kb(2, btn_tel='Телефон',
    btn_email='email',
    btn_website='Web-сайт',
    btn_vk='VK',
    btn_tgbot='Наш телеграм-бот'))

    @dp.callback_query(F.data == 'big_button_1_called')
    async def cb_handle_big_button_1_called(callback: CallbackQuery):
        if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1':
            await callback.message.edit_text(
                text='Была нажата БОЛЬШАЯ КНОПКА 1',
                reply_markup=callback.message.reply_markup
            )
        await callback.answer(text='ЭТО АЛЕРТ!', show_alert=True)


    @dp.callback_query(F.data.in_(['big_button_2_pressed']))
    async def cb_handle_big_button_2_pressed(callback: CallbackQuery):
        if callback.message.text != 'Нажата БОЛЬШАЯ КНОПКА 2':
            await callback.message.edit_text(
                text='Нажата БОЛЬШАЯ КНОПКА 2',
                reply_markup=callback.message.reply_markup
            )
        await callback.answer('Действие выполнено!')

    dp.callback_query(cb_handle_big_button_1_called, cb_handle_big_button_2_pressed)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
