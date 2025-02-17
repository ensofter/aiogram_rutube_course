from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Корзина'), KeyboardButton(text='Контакты')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)

inline_hi = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог', callback_data='catalog')],
        [InlineKeyboardButton(text='Корзина', callback_data='basket'),
            InlineKeyboardButton(text='Контакты', callback_data='contacts')]
])

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='YouTube', url='https://youtube.ru')]
    ]
)


cars = ['tesla', 'mercedes', 'bmw'] # обычно это запрос куда-то в бд


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url='https://ya.ru'))
    return keyboard.adjust(2).as_markup()  # as_markup обязательно добавляем


async def reply_cars():
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(1).as_markup()
