import asyncio
import logging
from environs import Env
from aiogram.filters import CommandStart

from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaDocument, InputMediaAudio
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder


logger = logging.getLogger(__name__)
config = Env()
config.read_env()
bot_token = config('BOT_TOKEN')


LEXICON = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'voice': '📢 Голосовуха',
    'video': '🎬 Видео',
    'video_note': 'Кружок',
    'document': '📑 Документ',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': 'AgACAgIAAxkBAAILDGfe1Q9dFeA6IH3rQCuzTtBCKq35AAJm7DEbmQj5Sk7cUEv_46I9AQADAgADeQADNgQ',
    'photo_id2': 'AgACAgIAAxkBAAILDmfe1UfWRSTjz74i36zA13v_amGOAAJq7DEbmQj5SnBohb16t9dZAQADAgADeQADNgQ',
    'voice_id1': 'AwACAgIAAxkBAAILEGfe1WQgVt0bYAP8YcKDtCLvO0nPAAKBbwACmQj5SoyQZLxkQ4dLNgQ',
    'voice_id2': 'AwACAgIAAxkBAAILEmfe1f6LxNBX_ifKRhJOscIieSAjAAKTbwACmQj5SnfGQCDzOmBtNgQ',
    'audio_id1': 'CQACAgIAAxkBAAILImfe2oZLh-YquCQ1BfXF0TzHFmU4AALdXgAC08wwSXqKxEdfowsSNgQ',
    'audio_id2': 'CQACAgIAAxkBAAILIGfe2ePyg-t8tyT9H1E5SfJhcqNvAALbbwACmQj5SnSiR5WrtcbANgQ',
    'document_id1': 'BQACAgIAAxkBAAILFGfe1hqTe-iti0hvPTT5b3I_K0_eAAKWbwACmQj5SqTFFwyobgGdNgQ',
    'document_id2': 'AAMCAgADGQEAAgsWZ97WMxgYf7_1KZ_bVA4uirxu5-cAAp9vAAKZCPlKZwjQVaVfrxIBAAdtAAM2BA',
    'video_id1': 'BAACAgIAAxkBAAILHGfe1xRLVog3pt1c_Pat5QAB4VhungACtG8AApkI-UrmS9URL996eDYE',
    'video_id2': 'BAACAgIAAxkBAAILHmfe1yENTVn_jRO5a4cVY9iH54JTAAK1bwACmQj5StDfrsSS9tggNgQ',
    'video_note_id1': 'DQACAgIAAxkBAAILGGfe1sxDAvzFxN2uH79pqHgGzspeAAKtbwACmQj5SpvF_Eq7fAK_NgQ',
    'video_note_id2': 'DQACAgIAAxkBAAILGmfe1u9U0FzCSEIBrNTn9bETYGZgAAKvbwACmQj5Sg0WU-sK1wUuNgQ'
}

def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()



async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - %(levelname)-8s %(filename)s:%(lineno)d '
                                                    '%(name)s - %(message)s')
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def handle_cmd_start(message: Message):
        markup = get_markup(2, 'voice')
        await message.answer_voice(
            voice=LEXICON['voice_id1'],
            caption='Это войс 1',
            reply_markup=markup
        )

    @dp.callback_query(F.data.in_(
        ['text', 'audio', 'video', 'document', 'photo', 'voice', 'video_note']
    ))
    async def handle_button_press(callback: CallbackQuery, bot: Bot):
        # markup = get_markup(2, 'text')
        # if callback.message.text == LEXICON['text_1']:
        #     text = LEXICON['text_2']
        # else:
        #     text = LEXICON['text_1']
        # await callback.message.edit_text(
        #     text=text,
        #     reply_markup=await markup
        # )
        # markup = get_markup(2, 'photo')
        # try:
        #     await bot.edit_message_media(
        #         chat_id=callback.message.chat.id,
        #         message_id=callback.message.message_id,
        #         media=InputMediaPhoto(
        #             media=LEXICON['photo_id2'],
        #             caption='Это фото 2'
        #         ),
        #         reply_markup=markup
        #     )
        # except TelegramBadRequest:
        #     await bot.edit_message_media(
        #         chat_id=callback.message.chat.id,
        #         message_id=callback.message.message_id,
        #         media=InputMediaPhoto(
        #             media=LEXICON['photo_id1'],
        #             caption='Это фото 1'
        #         ),
        #         reply_markup=markup
        #     )
        # markup = get_markup(2, 'document')
        # try:
        #     await bot.edit_message_media(
        #         chat_id=callback.message.chat.id,
        #         message_id=callback.message.message_id,
        #         media=InputMediaDocument(
        #             media=LEXICON['document_id2'],
        #             caption='Это документ 2'
        #         ),
        #         reply_markup=markup
        #     )
        # except TelegramBadRequest:
        #     await bot.edit_message_media(
        #         chat_id=callback.message.chat.id,
        #         message_id=callback.message.message_id,
        #         media=InputMediaDocument(
        #             media=LEXICON['document_id1'],
        #             caption='Это документ 1'
        #         ),
        #         reply_markup=markup
        #     )
        markup = get_markup(2, 'voice')
        try:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaAudio(
                    media=LEXICON['audio_id2'],
                    caption='Это аудио 2'
                ),
                reply_markup=markup
            )
        except TelegramBadRequest:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaAudio(
                    media=LEXICON['audio_id1'],
                    caption='Это аудио 1'
                ),
                reply_markup=markup
            )

    @dp.message()
    async def handle_every_message(message: Message):
        await message.answer(text='What the fuck')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


