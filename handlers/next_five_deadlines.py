from create_bot import dp
from aiogram.types import Message
from functions import is_user, take_variable
from create_data_base import DB


"""Модуль для регистрации основных текстовых команд"""

@dp.message_handler(regexp='Ближайшие 5 дедлайнов')
async def next_five(message: Message):
    """Показывает ближайшие 5 дедлайнов"""

    user_id = message.from_user.id
    if await is_user(user_id):
        await message.answer(await DB.show_next_n_deadline(await take_variable(user_id, 'group'), 5))


