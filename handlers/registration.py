from create_bot import dp
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from institutes_and_groups import registration_dictionary

"""Модуль для регистрации пользователя"""

async def make_registration_keyboard_institutes():
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    return kb

async def make_registration_keyboard_courses(institute):
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary[institute]:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    return kb

async def make_registration_keyboard_groups(institute, course):
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary[institute][course]:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    return kb

@dp.message_handler(commands=['reg'])
async def command_registration(message : Message):
    """Команда для выбора группы студента"""

    await message.answer("Выберите группу", reply_markup=await make_registration_keyboard_institutes())

@dp.callback_query_handler()