import logging

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import BaseFilter
from aiogram.types import Message
from environs import Env

env = Env()
env.read_env()

TOKEN = env('BOT_TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()


class IsDigitInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        if message.text:
            for word in message.text.split():
                normalize_word = word.replace('.', '').replace(',', '').strip()
                if normalize_word.isdigit():
                    numbers.append(int(normalize_word))
        if numbers:
            return {'numbers': numbers}
        else:
            return False


@dp.message(F.text.lower().startswith('найди числа'), IsDigitInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(
        text=f'Нашел: {", ".join(str(num) for num in numbers)}'
    )

@dp.message(F.text.lower().startswith('найди числа'))
async def precess_if_not_numbers(message: Message):
    await message.answer(
        text='Не нашел что-то'
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
