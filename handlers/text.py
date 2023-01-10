from create_bot import dp
from aiogram.types import Message
from functions import is_user, is_admin, take_variable, change_variable
from create_bot import DB
from date_variables import current_year, current_month, ru_month_array
from keyboards import make_calendar_keyboard

"""Модуль для регистрации основных текстовых команд"""

@dp.message_handler(regexp='Ближайшие 5 дедлайнов')
async def next_five(message: Message):
    """Показывает ближайшие 5 дедлайнов"""

    if is_user(message.from_user.id):
        await message.answer(DB.show_next_n_deadline(await take_variable(message.from_user.id, 'group'), 5))


