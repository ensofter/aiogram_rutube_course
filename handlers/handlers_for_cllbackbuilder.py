from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.inline_keyboar_for_callback_builer import markup
from aiogram.types import CallbackQuery
import logging
from callbacks.inline_callbacks_factory import MyCallBackExample

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def handle_cmd_start(message: Message):
    await message.answer(text='Вот такая клавиатура', reply_markup=markup)


# @router.callback_query()
# async def handle_any_inline_button_press(callback: CallbackQuery):
#     logger.debug(callback.model_dump_json(indent=4, exclude_none=True))
#     await callback.answer()


@router.callback_query(MyCallBackExample.filter())
async def handle_category_press(callback: CallbackQuery, callback_data: MyCallBackExample):
    await callback.message.answer(text=callback_data.pack())
    await callback.answer()