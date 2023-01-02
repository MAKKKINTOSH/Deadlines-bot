from create_bot import dp
from config import groups_array, callback_for_groups
from aiogram import types, Dispatcher
from keyboards import *
from functions import is_user
from asyncio import create_task

"""В модуле происходит обработка команд, введенных пользователем бота"""

@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    """Команда для начала использования бота"""

    await message.answer("Привет, я - прототип дедлайн бота\n\n"
                         "Чтобы узнать команды, используйте /help\n\n"
                         "Но для начала выберите группу")

    await message.answer("Выберите группу", reply_markup=make_registration_keyboard())

@dp.message_handler(commands=['reg'])
async def command_registration(message : types.Message):
    """Команда для выбора группы студента"""

    await message.answer("Выберите группу", reply_markup=make_registration_keyboard())

@dp.message_handler(commands=['menu'])
async def command_menu(message : types.Message):
    """Команда для вызова главного меню бота"""
    if is_user(message.from_user.id):
        await message.answer("Выберите действие", reply_markup=make_menu_keyboard(message.from_user.id))

@dp.message_handler(commands=['contacts'])
async def command_contacts(message : types.Message):
    """Команда для отправки пользователю контактов создателей бота (Я и Саша)"""

@dp.message_handler(commands=['help'])
async def command_help(message : types.Message):
    """Команда для помощи пользователю"""

#def register_handlers_commands(dp : Dispatcher):
#    dp.register_message_handler(command_menu, commands=['menu'])
#    dp.register_message_handler(command_registration, commands=['reg'])
#    dp.register_message_handler(command_help, commands=['help'])
#    dp.register_message_handler(command_start, commands=['start'])
#    dp.register_message_handler(command_contacts, commands=['contacts'])
