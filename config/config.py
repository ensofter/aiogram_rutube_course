from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    bot_token: str = None


@dataclass
class Config:
    tg_bot: TgBot= None


def load_config():
    config = Env()
    config.read_env()
    token = config('BOT_TOKEN')
    return Config(
        tg_bot=TgBot(bot_token=token)
    )
