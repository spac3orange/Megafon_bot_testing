from environs import Env
from loguru import logger
from dataclasses import dataclass
from aiogram import Bot

main_log_handler = logger.add("logs/main_log.log", rotation="100 MB", encoding='utf-8', level="INFO")
error_log_handler = logger.add("logs/errors.log", rotation="100 MB", encoding='utf-8', level="ERROR")


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    admin_id: str

    async def change_send_schedule(self, send_days: str, send_time: str) -> None:
        self.send_days = send_days
        self.send_time = send_time
        logger.info(f'Время оповещения изменено\nТекущее время оповещения {self.send_days} {self.send_time}')

    async def get_schedule(self):
        return self.send_days, self.send_time


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), admin_id=env('ADMIN_ID'))


config = load_config()
bot = Bot(token=config.tg_bot.token)
