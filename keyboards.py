from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from date_variables import current_month, current_year, days_array, callback_for_days
from functions import is_admin, take_variable
from users import main_admin
from create_bot import DB

"""Модуль для генерации клавиатур"""

cancel_button = InlineKeyboardButton("<<", callback_data="cancel")
cancel_keyboard = InlineKeyboardMarkup().add(cancel_button)
#Кнопка и клавиатура отмены

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


async def make_calendar_keyboard(group, month=current_month, year=current_year):
    """Клавиатура календарь"""

    keyboard = InlineKeyboardMarkup(row_width=6)
    quantity_of_days = int

    if month in [1, 3, 5, 6, 8, 10, 12]:
        quantity_of_days = 31
    elif month == 2 and year % 400 == 0:
        quantity_of_days = 29
    elif month == 2 and year % 100 == 0:
        quantity_of_days = 28
    elif month == 2 and year % 4 == 0:
        quantity_of_days = 29
    elif month == 2:
        quantity_of_days = 28
    else:
        quantity_of_days = 30

    b1 = InlineKeyboardButton('<<год<<', callback_data='previous_year')
    b2 = InlineKeyboardButton('>>год>>', callback_data='next_year')
    b3 = InlineKeyboardButton('<<месяц<<', callback_data='previous_month')
    b4 = InlineKeyboardButton('>>месяц>>', callback_data='next_month')

    keyboard.add(b1, b2)
    keyboard.add(b3, b4)
    text01 = "01" + 'ㅤ' if not await DB.record_exist(group, '01', month, year) else "01" + '☠'
    keyboard.add(InlineKeyboardButton(text01, callback_data="d01"))

    for k in range(1, quantity_of_days):
        text = days_array[k] + 'ㅤ' if not await DB.record_exist(group, days_array[k], month, year) else days_array[k] + '☠'
        keyboard.insert(InlineKeyboardButton(text, callback_data=callback_for_days[k]))

    for k in range(36 - quantity_of_days):
        keyboard.insert(InlineKeyboardButton(" ", callback_data=" "))

    keyboard.add(cancel_button)

    return keyboard

