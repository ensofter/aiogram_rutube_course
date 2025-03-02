from aiogram import Bot, Dispatcher
from aiogram.filters import BaseFilter
from aiogram.types import Message
from environs import Env


env = Env()
env.read_env()

TOKEN = env('BOT_TOKEN')
ADMIN_ID = env('ADMIN_ID')

bot = Bot(token=TOKEN)
dp = Dispatcher()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: [int]):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


class IsNumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        if numbers:
            return {'numbers': numbers}
        return False


bot_admins = [111, ADMIN_ID]

@dp.message(IsAdmin(bot_admins))
async def answer_only_to_admins(message: Message):
    print('!!!', message.from_user.id)
    await message.answer('Да, ты админ')


@dp.message()
async def answer_to_everybody(message: Message):
    print('!!!', message.from_user.id)
    await message.answer('Привет ты просто юзер')


if __name__ == '__main__':
    dp.run_polling(bot)



