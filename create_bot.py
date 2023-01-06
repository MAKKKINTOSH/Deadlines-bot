from aiogram import Bot, Dispatcher
from TOKEN import Token
from data_base import DataBase

"""Модуль инициализирует бота"""

bot = Bot(Token)
dp = Dispatcher(bot)
DB = DataBase("localhost", 3306, "root", "", "deadlines_data_base")

