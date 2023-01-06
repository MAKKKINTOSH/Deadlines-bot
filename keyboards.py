from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from functions import is_admin, take_variable

"""Модуль для генерации клавиатур"""

async def make_menu_keyboard(id):
    """Клавиатура главного меню"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Ближайшие 5 дедлайнов")
    b2 = KeyboardButton("Календарь")
    keyboard.add(b1, b2)
    if is_admin(id, take_variable(id, "group")):
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

async def make_registration_keyboard():
    """Клавиатура регистрации"""

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton
    b2 = InlineKeyboardButton
    b3 = InlineKeyboardButton
    for k in range(0, len(groups_array), 3):
        try:
            b1 = InlineKeyboardButton(text=groups_array[k],
                                      callback_data=groups_array[k])
            b2 = InlineKeyboardButton(text=groups_array[k+1],
                                      callback_data=groups_array[k+1])
            b3 = InlineKeyboardButton(text=groups_array[k+2],
                                      callback_data=groups_array[k+2])
        except:
            if len(groups_array) % 3 == 2:
                b3 = InlineKeyboardButton(text=" ", callback_data=" ")
            elif len(groups_array)%3 == 1:
                b2 = InlineKeyboardButton(text=" ", callback_data=" ")
                b3 = InlineKeyboardButton(text=" ", callback_data=" ")
        finally: keyboard.add(b1, b2, b3)

    return keyboard

async def make_calendar_keyboard(group, month=current_month, year=current_year):
    """Клавиатура календарь"""


