from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callbacks.inline_callbacks_factory import MyCallBackExample

button_1 = InlineKeyboardButton(
    text='Категория 1',
    callback_data=MyCallBackExample(
        category=1,
        sub_category=2,
        item_id=33
    ).pack()
)

button_2 = InlineKeyboardButton(
    text='Категория 2',
    callback_data=MyCallBackExample(
        category=2,
        sub_category=0,
        item_id=0
    ).pack()
)

markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_1], [button_2]
    ]
)
