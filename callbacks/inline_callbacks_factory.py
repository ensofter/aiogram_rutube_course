from aiogram.filters.callback_data import CallbackData



class MyCallBackExample(CallbackData, prefix='prem'):
    category: int
    sub_category: int
    item_id: int