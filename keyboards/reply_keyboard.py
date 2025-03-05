from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


button1 = KeyboardButton(text='Собака')
button2 = KeyboardButton(text='Огурцов')

keyboard = ReplyKeyboardMarkup(keyboard=[
    [button1, button2]],
    one_time_keyboard=True
)


keyboard_builder = ReplyKeyboardBuilder()

buttons = [KeyboardButton(text=f'Кнопка {i}') for i in range(1, 11)]
keyboard_builder.row(*buttons, width=4)

special_keyboard_builder = ReplyKeyboardBuilder()

contact_btn = KeyboardButton(
    text='Отправить контакт',
    request_contact=True
)
geo_btn = KeyboardButton(
    text='Отправить геопозицию',
    request_location=True
)
poll_btn = KeyboardButton(
    text='Создать опрос/векторину',
    request_poll=KeyboardButtonPollType()
)

special_keyboard_builder.row(contact_btn, geo_btn, poll_btn, width=1)