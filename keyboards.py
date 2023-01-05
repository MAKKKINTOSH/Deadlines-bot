from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from config import *

"""Модуль для генерации клавиатур"""

def make_menu_keyboard(id):
    """Клавиатура главного меню"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("Ближайшие 5 дедлайнов")
    b2 = KeyboardButton("Календарь")
    keyboard.add(b1, b2)


def make_cancel_keyboard(message):
    """Клавиатура для отмены действия и возврата в главное меню"""

def make_registration_keyboard():
    """Клавиатура регистрации"""
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton
    b2 = InlineKeyboardButton
    b3 = InlineKeyboardButton
    for k in range(0, len(groups_array), 3):
        try:
            b1 = InlineKeyboardButton(text=groups_array[k],
                                      callback_data=callback_for_groups[k])
            b2 = InlineKeyboardButton(text=groups_array[k+1],
                                      callback_data=callback_for_groups[k+1])
            b3 = InlineKeyboardButton(text=groups_array[k+2],
                                      callback_data=callback_for_groups[k+2])
        except:
            if len(groups_array) % 3 == 2:
                b3 = InlineKeyboardButton(text=" ", callback_data=" ")
            elif len(groups_array)%3 == 1:
                b2 = InlineKeyboardButton(text=" ", callback_data=" ")
                b3 = InlineKeyboardButton(text=" ", callback_data=" ")
        finally: keyboard.add(b1, b2, b3)

    return keyboard

def make_calendar_keyboard(group, month=current_month, year=current_year):
    """Клавиатура календарь"""