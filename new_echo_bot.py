from re import template
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command 
from aiogram.types import Message, ContentType, sticker
import logging
from environs import Env


env = Env()
env.read_env()


BOT_TOKEN = env('BOT_TOKEN')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def handle_start_command(message: Message):
    await message.answer('Привет! Я бот')


async def handle_help_command(message: Message):
    await message.answer('Команда помощи')


async def handle_every_message(message: Message):
    await message.reply(text=message.text)

async def handle_every_photo(message: Message):
    print('!!!', message.model_dump_json(indent=4, exclude_none=True))
    await message.reply_photo(message.photo[0].file_id)

async def handle_every_sticker(message: Message):
    print('!!!', message.model_dump_json(indent=4, exclude_none=True))
    await message.reply_sticker(sticker=message.sticker.file_id)


dp.message.register(handle_start_command, Command('start'))
dp.message.register(handle_help_command, Command('help'))
dp.message.register(handle_every_photo, F.photo)
dp.message.register(handle_every_sticker, F.sticker)
dp.message.register(handle_every_message)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}',
        style='{'
    )
    logging.getLogger(__name__)
    dp.run_polling(bot)

