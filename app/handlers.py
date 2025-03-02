from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb


from app.middlewares import TestMiddleWare

router = Router()

# внутренний мидлвари, работает только когда сообщение ловится фильтром (хэндлером)
router.message.middleware(TestMiddleWare())

#внешний мидлвари, отрабатывает ВСЕГДА
#router.message.outer_middleware(TestMiddleWare())


class Reg(StatesGroup):
    name = State()
    number = State()


@router.message(CommandStart())
async def cmd_start_command(message: Message):
    await message.reply(f'Hello! your ID: {message.from_user.id}\nТвое имя: {message.from_user.full_name}',
                        reply_markup=kb.main)


@router.message(Command('hi'))
async def cmd_hi(message: Message):
    await message.reply('Some message to me', reply_markup=kb.inline_hi)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог')
    await callback.message.edit_text('Это каталог', reply_markup=await kb.inline_cars())


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help', reply_markup=kb.settings)


@router.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.answer('Ok!', reply_markup=await kb.inline_cars())


@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото {message.photo[-1]}')


@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIGI2euWEjmH1j43wliiAOCVRrQXYahAAL-9DEbGr9xSdBym0U0sAMXAQADAgADeQADNgQ',
        caption='This is your photo')


@router.message(Command(commands=['reg']))
async def reg_get_name(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя')


@router.message(Reg.name)
async def reg_set_name_and_get_number(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')


@router.message(Reg.number)
async def reg_set_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer('Спасибо за регистрацию')
    await message.answer(f'Ваше имя {data["name"]} и ваш номер {data["number"]}')
    await state.clear()
