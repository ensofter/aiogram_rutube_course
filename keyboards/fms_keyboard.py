from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.fsm_lexicon import LEXICON_RU


def create_inline_kb(width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON_RU[button] if button in LEXICON_RU else button,
                    callback_data=button
                )
            )

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=button
                )
            )

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
