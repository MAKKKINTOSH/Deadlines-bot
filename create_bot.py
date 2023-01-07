from aiogram import Bot, Dispatcher
from TOKEN import Token
from data_base import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage

"""Модуль инициализирует бота"""

bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())
DB = DataBase("localhost", 3306, "root", "", "deadlines_data_base")

