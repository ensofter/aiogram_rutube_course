import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start_command(message: Message):
    await message.reply(f'Hello! your ID: {message.from_user.id}\nТвое имя: {message.from_user.full_name}')


@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')


@dp.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.answer('Ok!')


@dp.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото {message.photo[-1]}')


@dp.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAIGI2euWEjmH1j43wliiAOCVRrQXYahAAL-9DEbGr9xSdBym0U0sAMXAQADAgADeQADNgQ',
                               caption='This is your photo')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
