from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    bot_token: str = None


@dataclass
class Db:
    db_url: str = None


@dataclass
class Config:
    tg_bot: TgBot = None
    db: Db = None


def load_config():
    config = Env()
    config.read_env()
    token = config('BOT_TOKEN')
    db_url = config('DB_URL')
    return Config(
        tg_bot=TgBot(
            bot_token=token
        ),
        db=Db(
            db_url=db_url
        )
    )
