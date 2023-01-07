from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from institutes_and_groups import groups_array
from functions import is_admin, take_variable

"""Модуль для генерации клавиатур"""

async def make_menu_keyboard(id):
    """Клавиатура главного меню"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Ближайшие 5 дедлайнов")
    b2 = KeyboardButton("Календарь")
    keyboard.add(b1, b2)
    if await is_admin(id, await take_variable(id, "group")):
        b3 = KeyboardButton("Добавить")
        b4 = KeyboardButton("Удалить")
        keyboard.add(b3, b4)
    if id == main_admin:
        keyboard.add(KeyboardButton("Внести админа"))

    return keyboard

async def make_cancel_keyboard():
    """Клавиатура для отмены действия и возврата в главное меню"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("<<", callback_data="cancel"))
    return keyboard

async def make_calendar_keyboard(group, month=current_month, year=current_year):
    """Клавиатура календарь"""


