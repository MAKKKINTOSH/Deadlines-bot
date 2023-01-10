from create_bot import dp, DB
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from functions import is_user, is_admin, take_variable
from date_variables import callback_for_days, current_month, current_year, ru_month_array, month_array
from keyboards import make_calendar_keyboard
from datetime import datetime

"""Модуль включает в себя календарь, добавление, показ и удаление дедлайнов через него"""


class FSM_show(StatesGroup):
    show_show_calendar = State()


class FSM_add(StatesGroup):
    show_add_calendar = State()
    add_deadline = State()


class FSM_delete(StatesGroup):
    show_delete_calendar = State()
    delete_deadline = State()


async def change_month(month, operator):
    if month == 12 and operator == '+':
        return 1
    elif month == 1 and operator == '-':
        return 12
    return (month - 1) if operator == "-" else (month + 1)


@dp.message_handler(regexp="Календарь", state=None)
async def show_show_calendar(message: Message, state: FSMContext):
    """Выводит календарь для просмотра дедлайнов"""

    global current_year, current_month
    current_year = datetime.now().year
    current_month = datetime.now().month

    user_id = message.from_user.id
    if await is_user(user_id):
        async with state.proxy() as storage:

            storage['year'] = current_year
            storage['month'] = current_month
            await message.answer(f"Выберите дату, на которую хотите посмотреть дедлайн\n\n"
                                 f"Группа: {str(await take_variable(user_id, 'group')).replace('_', '-')}\n"
                                 f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                                 reply_markup=await make_calendar_keyboard(await take_variable(user_id, 'group')))
            await FSM_show.show_show_calendar.set()


@dp.callback_query_handler(text=callback_for_days, state=FSM_show.show_show_calendar)
async def show_deadline(call: CallbackQuery, state: FSMContext):
    """Показывает дедлайны по дате, выбранной в календаре"""

    async with state.proxy() as storage:

        set_group = await take_variable(call.from_user.id, 'group')
        set_day = call.data[1:]
        set_month = storage['month']
        set_year = storage['year']

        await call.message.edit_text(await DB.show_deadline(set_group, set_day, set_month, set_year))
        await call.answer()
        await state.finish()


@dp.message_handler(regexp="Добавить", state=None)
async def show_add_calendar(message: Message, state: FSMContext):
    """Выводит календарь для добавления дедлайнов"""

    user_id = message.from_user.id
    if await is_user(user_id):
        if await is_admin(user_id, await take_variable(user_id, 'group')):
            async with state.proxy() as storage:

                storage['month'] = current_month
                storage['year'] = current_year
                await message.answer(f"Выберите дату, на которую хотите добавить дедлайн\n\n"
                                     f"Группа: {str(await take_variable(user_id, 'group')).replace('_', '-')}\n"
                                     f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                                     reply_markup=await make_calendar_keyboard(await take_variable(user_id, 'group')))
                await FSM_add.show_add_calendar.set()


@dp.callback_query_handler(text=callback_for_days, state=FSM_add.show_add_calendar)
async def select_date_to_add(call: CallbackQuery, state: FSMContext):
    """Выбрана дата для добавления дедлайна"""

    async with state.proxy() as storage:
        set_day = call.data[1:]
        storage['day'] = set_day
        set_month = storage['month']
        set_year = storage['year']

        await call.message.edit_text(f"Введите дедлайн на {set_day}.{set_month}.{set_year}")
        await FSM_add.next()
        await call.answer()


@dp.message_handler(content_types=["text"], state=FSM_add.add_deadline)
async def make_deadline(message: Message, state: FSMContext):
    """Добавляет дедлайн"""

    async with state.proxy() as storage:
        await DB.make_deadline(await take_variable(message.chat.id, "group"),
                         storage['day'],
                         storage['month'],
                         storage['year'],
                         message.text)
        await message.answer("Дедлайн внесен")
        await state.finish()


@dp.message_handler(regexp="Удалить", state=None)
async def show_delete_calendar(message: Message, state: FSMContext):
    """Выводит календарь для удаления дедлайнов"""

    user_id = message.from_user.id
    if await is_user(user_id):
        if await is_admin(user_id, await take_variable(user_id, 'group')):
            async with state.proxy() as storage:

                storage['month'] = current_month
                storage['year'] = current_year
                await message.answer(f"Выберите дату, на которую хотите удалить дедлайн\n\n"
                                     f"Группа: {str(await take_variable(user_id, 'group')).replace('_', '-')}\n"
                                     f"Год: {current_year}\nМесяц: {ru_month_array[current_month - 1]}",
                                     reply_markup=await make_calendar_keyboard(await take_variable(user_id, 'group')))
                await FSM_delete.show_delete_calendar.set()

@dp.callback_query_handler(text = callback_for_days, state=FSM_delete.show_delete_calendar)
async def select_date_for_delete(call: CallbackQuery, state: FSMContext):
    """Выводит дедлайны на указанную дату для последующего удаления"""
    async with state.proxy() as storage:

        set_group = await take_variable(call.from_user.id, 'group')
        set_day = call.data[1:]
        storage['day'] = set_day
        set_month = storage['month']
        set_year = storage['year']

        await call.message.edit_text(f"{await DB.show_deadline(set_group, set_day, set_month, set_year)}\n\n"
                                     f"Введите номер дедлайна, который хотите удалить")
        await FSM_delete.next()
        await call.answer()

@dp.message_handler(content_types="text", state=FSM_delete.delete_deadline)
async def delete_deadline(message: Message, state: FSMContext):
    """Удаляет дедлайн по введенному номеру"""

    async with state.proxy() as storage:
        try:
            await DB.delete_deadline(await take_variable(message.from_user.id, 'group'),
                               storage['day'],
                               storage['month'],
                               storage['year'],
                               int(message.text))
            await message.answer("✅Отлично, дедлайн успешно удален✅")
        except:
            await message.answer("🚫Ошибка, вы неправильно ввели номер🚫")
    await state.finish()


@dp.callback_query_handler(text=['previous_year', 'next_year', 'previous_month', 'next_month'], state="*")
async def change_data(call: CallbackQuery, state: FSMContext):
    """Изменяет дату в календаре"""

    async with state.proxy() as storage:
        if call.data == 'previous_year':
            storage['year'] = storage['year'] - 1

        elif call.data == 'next_year':
            storage['year'] = storage['year'] + 1

        elif call.data == 'previous_month':
            storage['month'] = await change_month(storage['month'], '-')

        else:
            storage['month'] = await change_month(storage['month'], '+')

        current_state = await state.get_state()

        if current_state == FSM_show.show_show_calendar:
            text = "Выберите дату, на которую хотите посмотреть дедлайн"
        elif current_state == FSM_add.show_add_calendar:
            text = "Выберите дату, на которую хотите добавить дедлайн"
        else:
            text = "Выберите дату, на которую хотите удалить дедлайн"

        year = storage['year']
        month = storage['month']
        user_id = call.from_user.id
        await call.message.edit_text(f"{text}\n\n"
                              f"Группа: {str(await take_variable(user_id, 'group')).replace('_', '-')}\n"
                              f"Год: {year}\n"
                              f"Месяц: {ru_month_array[month-1]}",
                              reply_markup=await make_calendar_keyboard(await take_variable(user_id, 'group'),month, year))

@dp.callback_query_handler(text="cancel", state=[FSM_show, FSM_add, FSM_delete])
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Действие отменено")
    await call.answer()
    await state.finish()


