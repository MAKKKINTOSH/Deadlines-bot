from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import current_month, current_year, main_admin, days_array, callback_for_days
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

    current = 0
    DBR = []

    for k in range(quantity_of_days // 6):
        for k in range(6):
            text = days_array[current]

            DBR += [InlineKeyboardButton(text, callback_data=callback_for_days[current])]
            current += 1
        keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3], DBR[4], DBR[5])
        DBR = []

    for k in range(quantity_of_days % 6):
        text = days_array[current]

        DBR += [InlineKeyboardButton(text, callback_data=callback_for_days[current])]
        current += 1

    if quantity_of_days % 6 == 1: keyboard.add(DBR[0])
    if quantity_of_days % 6 == 4: keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3])
    if quantity_of_days % 6 == 5: keyboard.add(DBR[0], DBR[1], DBR[2], DBR[3], DBR[4])

    keyboard.add(InlineKeyboardButton("<<", callback_data="cancel"))

    return keyboard

