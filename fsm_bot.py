import asyncio
import logging
from functools import partial

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, PhotoSize
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import load_config
from database.engine import DatabaseManager
from database.orm_query import orm_add_user, orm_get_user, orm_update_user
from keyboards.fms_keyboard import create_inline_kb
from lexicon.fsm_lexicon import LEXICON_RU
from middleware.db import DataBaseSession

conf = load_config()

logger = logging.getLogger(__name__)


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    upload_photo = State()
    fill_education = State()
    fill_wish_news = State()


async def on_startup(bot: Bot, db_manager: DatabaseManager):
    await db_manager.create_db()


async def on_shutdown(bot: Bot):
    print('bot лег')


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(levelname)-8s %(filename)s:%(lineno)d '
                                                    '%(name)s - %(message)s')
    storage = MemoryStorage()

    bot = Bot(conf.tg_bot.bot_token)
    dp = Dispatcher(storage=storage)

    db_manager = DatabaseManager(conf.db.db_url)

    dp.startup.register(partial(on_startup, bot, db_manager))
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=db_manager.session_maker))

    @dp.message(CommandStart())
    async def handle_cmd_start(message: Message, session: AsyncSession):
        user = await orm_get_user(session, message.from_user.id)
        if user is None:
            await orm_add_user(session, message.from_user.id)

        logger.debug('!!! what the fuck')
        await message.answer(
            text=LEXICON_RU['/start']
        )

    @dp.message(Command(commands='cancel'), StateFilter(default_state))
    async def handle_cmd_cancel(message: Message):
        await message.answer(
            text=LEXICON_RU['/cancel']
        )

    @dp.message(Command(commands='cancel'), ~StateFilter(default_state))
    async def handle_cmd_cancel_in_state(message: Message, state: FSMContext):
        await message.answer(
            text=LEXICON_RU['/cancel_in_state']
        )
        await state.clear()

    @dp.message(Command(commands='fillform'), StateFilter(default_state))
    async def handle_cmd_fillform(message: Message, state: FSMContext):
        await message.answer(text=LEXICON_RU['/fillform'])
        await state.set_state(FSMFillForm.fill_name)

    @dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
    async def handle_fsm_name_sent(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer(text=LEXICON_RU['give_age'])
        await state.set_state(FSMFillForm.fill_age)

    @dp.message(StateFilter(FSMFillForm.fill_name))
    async def warning_not_name(message: Message):
        await message.answer(
            text=LEXICON_RU['warning_not_name']
        )

    @dp.message(StateFilter(FSMFillForm.fill_age), lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
    async def handle_fsm_age_sent(message: Message, state: FSMContext):
        await state.update_data(age=message.text)

        kb = create_inline_kb(2, 'male', 'female', 'undefined_gender')

        await message.answer(
            text=LEXICON_RU['gender'],
            reply_markup=kb
        )

        await state.set_state(FSMFillForm.fill_gender)

    @dp.message(StateFilter(FSMFillForm.fill_age))
    async def warning_not_age(message: Message):
        await message.answer(
            text=LEXICON_RU['warning_not_age']
        )

    @dp.callback_query(StateFilter(FSMFillForm.fill_gender),
                       F.data.in_(['male', 'female', 'undefined_gender']))
    async def handle_fsm_gender_pressed(callback: CallbackQuery, state: FSMContext):
        await state.update_data(gender=callback.data)
        await callback.message.delete()
        await callback.message.answer(
            text=LEXICON_RU['photo']
        )
        await state.set_state(FSMFillForm.upload_photo)

    @dp.message(StateFilter(FSMFillForm.fill_gender))
    async def warning_not_gender(message: Message):
        await message.answer(
            text=LEXICON_RU['warning_not_gender']
        )

    @dp.message(StateFilter(FSMFillForm.upload_photo), F.photo[-1].as_('largest_photo'))
    async def handle_fsm_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
        await state.update_data(
            photo_unique_id=largest_photo.file_unique_id,
            photo_id=largest_photo.file_id
        )
        kb = create_inline_kb(2, 'secondary', 'higher', 'no_edu')
        await message.answer(
            text=LEXICON_RU['education'],
            reply_markup=kb
        )
        await state.set_state(FSMFillForm.fill_education)

    @dp.message(StateFilter(FSMFillForm.upload_photo))
    async def warning_not_photo(message: Message):
        await message.answer(
            text=LEXICON_RU['warning_no_photo']
        )

    @dp.callback_query(StateFilter(FSMFillForm.fill_education), F.data.in_(['secondary', 'higher', 'no_edu']))
    async def handle_fsm_education_pressed(callback: CallbackQuery, state: FSMContext):
        await state.update_data(education=callback.data)
        kb = create_inline_kb(1, 'yes_news', 'no_news')
        await callback.message.edit_text(
            text=LEXICON_RU['get_news'],
            reply_markup=kb
        )
        await state.set_state(FSMFillForm.fill_wish_news)

    @dp.message(StateFilter(FSMFillForm.fill_education))
    async def warning_not_education(message: Message):
        await message.answer(
            text=LEXICON_RU['warning_no_education']
        )

    @dp.callback_query(StateFilter(FSMFillForm.fill_wish_news), F.data.in_(['yes_news', 'no_news']))
    async def handle_fsm_news_pressed(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        await state.update_data(wish_news=callback.data == 'yes_news')

        data = await state.get_data()
        await orm_update_user(session, callback.from_user.id, data)

        await state.clear()

        await callback.message.edit_text(
            text=LEXICON_RU['questionare_end']
        )
        await callback.message.answer(
            text=LEXICON_RU['get_my_data']
        )

    @dp.message(StateFilter(FSMFillForm.fill_wish_news))
    async def warning_not_news(message: Message):
        await message.answer(
            text=LEXICON_RU['warning_not_news']
        )

    @dp.message(Command(commands='showdata'), StateFilter(default_state))
    async def handle_cmd_showdata(message: Message, session: AsyncSession):
        user = await orm_get_user(session, message.from_user.id)
        if user:
            await message.answer_photo(
                photo=user.photo,
                caption=f'Имя: {user.name}\n'
                        f'Возраст: {user.age}\n'
                        f'Пол: {user.gender}\n'
                        f'Образование: {user.education}\n'
                        f'Получать новости: {user.wish_news}\n'
                        f'Забанен: {user.is_hold}\n'
            )
        else:
            await message.answer(
                text=LEXICON_RU['no_profile']
            )

    @dp.message(StateFilter(default_state))
    async def handle_every_message(message: Message):
        await message.answer('hello motherfucker')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
