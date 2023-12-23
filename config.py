import os
from dataclasses import dataclass
from typing import Union

from environs import Env
from dotenv import load_dotenv


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм боту


@dataclass
class Config:
    tg_bot: TgBot  # Телеграм бот


# Функция загрузки конфигурации
def load_config(path: Union[str, None] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env("BOT_TOKEN")))


# Загрузите переменные окружения из файла .env
load_dotenv()

# Получение значения переменной ADMIN_IDS
admin_ids_str = os.getenv("ADMIN_IDS")

# Преобразование строки в список разрешенных ID
allowed_user_ids = [int(admin_id) for admin_id in admin_ids_str.split(',')]

