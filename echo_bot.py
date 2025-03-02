from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import logging
from environs import Env

env = Env()
env.read_env()


BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Hello!\nMy name is echo bot!\nWrite to me something!')


@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Write to me something and i reply you this')


@dp.message()
async def send_echo(message: Message):
    try:
        print('!!!', message.model_dump_json(indent=4, exclude_none=True))
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
                text='Данный тип апдейтов не поддерживается\nметодом send_copy'
        )
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    dp.run_polling(bot)
