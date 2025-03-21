import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, F
from environs import Env
from aiogram.filters import CommandStart

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

config = Env()
config.read_env()
bot_token = config('BOT_TOKEN')

logger = logging.getLogger(__name__)

jokes: dict[int, str] = {
    1: 'с хабра, описание фильмов Матрица\n\nСудя по всему, в городе машин либо очень либеральный мэр, либо очень криворукие сисадмины. Иначе как объяснить, что свободные люди беспрепятственно подключаются к вражеской ИТ-системе? Причем удаленно из тарантаса, летающего по канализации! Т.е. мало того, что у машин в сточных трубах развернут высокоскоростной Wi-Fi, так они еще и пускают в свою сеть всех подряд, позволяя неавторизованным пользователям получать данные из системы, вносить в нее изменения и общаться между собой. Красота!',
    2: '- У меня на одном курсе был фин, он приехал к нам т.к. был очарован культурой гопников. Он хотел проникнуться ею у первоисточника и подтянуть мат. И вот где-то в Питере он припал к истокам, все-все выучил и загорелся желанием принести культуру другим иностранцам группы. А там были бразильцы, немцы итальянцы, французы и китаец. И вот захожу как-то я в группу и там хором повторяют слова "ъуъ" и "съка" с шестью разными акцентами.\n- Хотелось бы послушать, как они говорили "ъуъ"',
    3: 'Я в восторге от наших учителей.\nСыну в школе дали домашнее задание, где, среди прочего, был вопрос "как связаны буква А4 и бык?"\nРассказал ему про финикийский алфавит, как первую фонетическую письменность. Что там была буква "алеф", очень похожая на нашу современную "А", и что слово "алеф" означало "бык". Что, возможно, букву так назвали, потому что если развернуть ее, то она похожа на морду быка с рогами.\nЕще очень радовался, что детям во втором классе такие вещи рассказывают.\nУчительница поставила ребенку двойку, заявив, что он фантазировал в домашнем задании. А правильный ответ: если к слову "бык" добавить "а", получится родительный падеж.\nЯ не планировал в таком раннем возрасте рассказывать сыну, что половина окружающих людей - идиоты, но, видимо, придется :-)',
    4: 'у меня на балконе сосулька растет метровая, прямо над машиной, которая ссигналит каждую ночь. Я эту сосульку из распылителя подкармливаю.',
    5: 'xx: Мне сейчас спам пришел "Я живу в доме напротив, вот моя ссылка *адрес ссылки*. Давай познакомимся". Я ответил, что живу напротив морга и меня пугают такие знакомства',
    6: 'xxx: В командировке на съемной квартире нужна была марля, чтобы погладить футболку. Начал шариться по всем ящикам. Марлю не нашел, зато нашел ключ в шкафу между простынями. Вспомнил, что один ящик в этом шкафу был заперт. Попробовал открыть его найденным ключом. Открыл. Внутри нашел марлю. Не зря в квесты играл..'
}


def random_joke_number():
    return random.randint(1, len(jokes))


async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d '
                                                    '%(name)s:%(message)s')
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    more_button = InlineKeyboardButton(
        text='Еще шутку',
        callback_data='more_jokes'
    )

    more_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                more_button
            ]
        ]
    )

    @dp.message(CommandStart())
    async def handle_cmd_start(message: Message):
        await message.answer(
            text=jokes[random_joke_number()],
            reply_markup=more_markup
        )

    @dp.callback_query(F.data == 'more_jokes')
    async def handle_more_button(callback: CallbackQuery):
        # await callback.message.delete()
        await callback.message.edit_text(
            text=jokes[random_joke_number()],
            reply_markup=more_markup
        )


    @dp.message()
    async def handle_every_message(message: Message):
        await message.answer(text='what the fuck?')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
