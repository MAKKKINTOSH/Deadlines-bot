from aiogram import Bot, Dispatcher
from config import Token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

"""Модуль инициализирует бота"""

bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

