from create_bot import dp
from aiogram.types import Message
from functions import is_user, is_admin, delete_previous_calendar, take_variable, change_variable
from create_bot import DB
from config import current_year, current_month, ru_month_array
from keyboards import make_calendar_keyboard

"""Модуль для регистрации основных текстовых команд"""

@dp.message_handler(regexp='Ближайшие 5 дедлайнов')
async def next_five(message: Message):
    """Показывает ближайшие 5 дедлайнов"""

    if is_user(message.from_user.id):
        await delete_previous_calendar(message.from_user.id, message.message_id)
        await message.answer(DB.show_next_n_deadline(await take_variable(message.from_user.id, 'group'), 5))

@dp.message_handler(regexp='Календарь')
async def calendar(message: Message):
    """Выводит календарь для просмотра дедлайнов"""

    user_id = message.from_user.id
    if is_user(user_id):
        await delete_previous_calendar(message.from_user.id, message.message_id)

        await change_variable(user_id, "edit_type", 0)
        await change_variable(user_id, "year", current_year)
        await change_variable(user_id, "month", current_month)

        await message.answer(f"Выберите дату, на которую хотите посмотреть дедлайн\n\n"
                         f"Группа: {take_variable(user_id, 'group')}\n"
                         f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                         reply_markup=await make_calendar_keyboard(take_variable(user_id, 'group')))

@dp.message_handler(regexp='Добавить')
async def add(message: Message):
    """Добавляет дедлайн через календарь"""

    user_id = message.from_user.id
    if is_user(user_id):
        if is_admin(user_id, await take_variable(user_id, 'group')):
            await delete_previous_calendar(message.from_user.id, message.message_id)

            await change_variable(user_id, 'edit_type', 1)
            await change_variable(user_id, "year", current_year)
            await change_variable(user_id, "month", current_month)

            await message.answer(f"Выберите дату, на которую хотите добавить дедлайн дедлайн\n\n"
                                 f"Группа: {take_variable(user_id, 'group')}\n"
                                 f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                                 reply_markup=await make_calendar_keyboard(take_variable(user_id, 'group')))

@dp.message_handler(regexp='Удалить')
async def delete(message: Message):
    """Удаляет дедлайн через календарь"""

    user_id = message.from_user.id
    if is_user(user_id):
        if is_admin(user_id, await take_variable(user_id, 'group')):
            await delete_previous_calendar(message.from_user.id, message.message_id)

            await change_variable(user_id, 'edit_type', 2)
            await change_variable(user_id, "year", current_year)
            await change_variable(user_id, "month", current_month)

            await message.answer(f"Выберите дату, на которую хотите добавить дедлайн дедлайн\n\n"
                                 f"Группа: {take_variable(user_id, 'group')}\n"
                                 f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                                 reply_markup=await make_calendar_keyboard(take_variable(user_id, 'group')))

