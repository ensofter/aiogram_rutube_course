from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from keyboards import reply_keyboard

router = Router()


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    await message.answer(
        text='Чего кошки боятся?',
        reply_markup=reply_keyboard.keyboard
    )


@router.message(Command(commands=['help']))
async def handle_cmd_help(message: Message):
    await message.answer(
        text='Тут будут все кнопки',
        reply_markup=reply_keyboard.keyboard_builder.as_markup(resize_keyboard=True)
    )


@router.message(Command(commands=['special']))
async def handle_cmd_special(message: Message):
    await message.answer(
        text='Выбери специальную кнопку',
        reply_markup=reply_keyboard.special_keyboard_builder.as_markup(resize_keyboard=True,
                                                                       one_tiem_keyboard=True,
                                                                       input_field_placeholder='Wow its placeholder')
    )


@router.message(F.text == 'Собака')
async def handle_dog_answer(message: Message):
    await message.answer(
        text='Да, кошки боятся собак!',
        reply_markup=ReplyKeyboardRemove()
    )
