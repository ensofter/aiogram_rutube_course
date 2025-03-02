from aiofiles.threadpool import text
from aiogram import Bot, Dispatcher, F
from aiogram.methods import answer_callback_query
from aiogram.types import Message
from aiogram.filters import Command
import random
import logging
from dataclasses import dataclass
from environs import Env


env = Env()
env.read_env()


TOKEN = env('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = {}


@dataclass
class User:
    in_game: bool = False
    secret_number: int = None
    attempts: int = 0
    total_games: int = 0
    wins: int = 0


def get_random_number() -> int:
    return random.randint(1, 11)


@dp.message(Command('start'))
async def handle_cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = User(in_game=False, attempts=0, total_games=0, wins=0)
        await message.answer(
            text='Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
                 'Чтобы получить правила игры и список доступных '
                 'команд - отправьте команду /help')
    else:
        if users[user_id].in_game:
            await message.answer(
                text=f'Мы пока что в игре и я могу обрабатывать только числа от 1 до 10, а так же команды '
                '/cancel и /stat')
        else:
            await message.answer(text='Ты пока не начал играть. Чтобы ознакомиться с правилами отправь команду /help')


@dp.message(Command('help'))
async def handle_cmd_help(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        await message.answer(
            text=f'Правила игры:\n\nЯ загадываю число от 1 до 10, '
            f'а вам нужно его угадать\nУ вас есть {users[user_id].attempts} '
            'попыток\n\nДоступные команды:\n/help - правила '
            'игры и список команд\n/cancel - выйти из игры\n'
            '/stat - посмотреть статистику\n\nДавай сыграем?')
    else:
        await message.answer(text='Чтобы начать отправьте конмаду /start')


@dp.message(Command('stat'))
async def handle_cmd_stat(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        await message.answer(
            text=f'in game - {users[user_id].in_game}\n'
            f'attempt - {users[user_id].attempts}\n'
            f'total_games - {users[user_id].total_games}\n'
            f'wins - {users[user_id].wins}'
        )
    else:
        await message.answer(text='Ты еще не начал играть! Чтобы начать отправь /start')


@dp.message(Command('cancel'))
async def handle_cmd_cancel(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id].in_game:
            users[user_id].in_game = False
            await message.answer(
                text='Вы вышли из игры. Если захотите сыграть снова - напишите об этом'
            )
        else:
            await message.answer(
                text='А мы и так с тобой не играем. Может, сыграем разок?'
            )
    else:
        await message.answer(text='Ты еще не начал играть! Чтобы начать отправь /start')


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def handle_user_accept(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id].in_game:
            await message.answer(
                text='Мы пока что в игре и я могу обрабатывать только числа от 1 до 10, а так же команды '
                     '/cancel и /stat'
            )
        else:
            users[user_id].in_game = True
            users[user_id].secret_number = get_random_number()
            users[user_id].attempts = 5
            users[user_id].total_games += 1
            await message.answer(
                text='Ура!\n\nЯ загадал число от 1 до 10, попробуй угадать!'
            )
    else:
        await message.answer(text=f'Ты еще не в игре. Чтобы начать набери /start')


@dp.message(lambda x: x.text and x.text.isdigit() and (1 <= int(x.text) <= 10))
async def handle_every_message(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id].in_game:
            if int(message.text) == users[user_id].secret_number:
                users[user_id].in_game = False
                users[user_id].wins += 1
                await message.answer(
                    text='Ура!!! Вы угадали число!\n\n'
                    'Может, сыграем еще?'
                )
            elif int(message.text) > users[user_id].secret_number and users[user_id].attempts > 0:
                users[user_id].attempts -= 1
                await message.answer(text='Мое число меньше')
            elif int(message.text) < users[user_id].secret_number and users[user_id].attempts > 0:
                users[user_id].attempts -= 1
                await message.answer(text='Мое число больше')

            if users[user_id].attempts == 0:
                users[user_id].in_game = False
                await message.answer(
                    text='К сожалению, у вас больше не осталось '
                    'попыток. Вы проиграли :(\n\nМое число '
                    f'было {users[user_id].secret_number}\n\nДавайте '
                    'сыграем еще?'
                )
        else:
            await message.answer(text='Давай сыграем?')
    else:
        await message.answer(text='Чтобы начать игру нажми /start')


@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def handle_user_refuse(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id].in_game:
            await message.answer(text='Вообще-то мы играет, присылай цифры')
        else:
            await message.answer(text='Жаль, ну ты же захочешь попозже поиграть?')
    else:
        await message.answer(text='Ты еще даже не начинал!\n /start для начала')


@dp.message()
async def handle_every_message(message: Message):
    user_id = message.from_user.id
    if user_id in users:
        if users[user_id].in_game:
            await message.answer(text='Давай уж лучше ты цифры будешь присылать')
        else:
            await message.answer(text='Ты хочешь поиграть?')
    else:
        await message.answer(text='Чтобы начать игру просто отправь /start')


        
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
