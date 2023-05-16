from create_bot import dp
from create_data_base import DB
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from data.institutes_and_groups import registration_dictionary, institutes, courses, groups_array, institutes_callback
from data.users import users
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import  State, StatesGroup
from datetime import datetime
from keyboards import cancel_button, make_menu_keyboard

"""Модуль для регистрации пользователя"""

class FSM_registration(StatesGroup):
    institute = State()
    course = State()
    group = State()

async def make_registration_keyboard_institutes():
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary:
        kb.add(InlineKeyboardButton(k, callback_data=institutes_callback[k]))
    kb.add(cancel_button)
    return kb

async def make_registration_keyboard_courses(institute):
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary[institute]:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    kb.add(cancel_button)
    return kb

async def make_registration_keyboard_groups(institute, course):
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary[institute][course]:
        kb.add(InlineKeyboardButton(k.replace("_", "-"), callback_data=k))
    kb.add(cancel_button)
    return kb

@dp.message_handler(commands = ['reg'], state=None)
async def command_registration(message: Message):
    """Команда для выбора группы студента"""

    await FSM_registration.institute.set()
    await message.answer("Выберите институт", reply_markup=await make_registration_keyboard_institutes())
    print(message.from_user.id, datetime.now().hour, datetime.now().minute)

@dp.callback_query_handler(text = list(institutes_callback.values()), state=FSM_registration.institute)
async def chosen_institute(call: CallbackQuery, state: FSMContext):
    """Выбор курса"""

    async with state.proxy() as storage:
        storage['institute'] = institutes[call.data]
    await FSM_registration.next()
    await call.message.edit_text("Выберите курс", reply_markup= await make_registration_keyboard_courses(institutes[call.data]))
    await call.answer()

@dp.callback_query_handler(text = courses, state=FSM_registration.course)
async def chosen_course(call: CallbackQuery, state: FSMContext):
    """Выбор группы"""

    async with state.proxy() as storage:
        storage['course'] = call.data
    await FSM_registration.next()
    await call.message.edit_text("Выберите группу", reply_markup= await make_registration_keyboard_groups(storage['institute'], call.data))
    await call.answer()

@dp.callback_query_handler(text = groups_array, state=FSM_registration.group)
async def chosen_group(call: CallbackQuery, state: FSMContext):
    """Внесение пользователя в базу данных"""
    
    global users
    user_id = call.from_user.id
    async with state.proxy() as storage:
        await DB.make_user(user_id, call.data)

        for k in range(len(users)):
            if users[k]['user_id'] == user_id:
                users.pop(k)
                break

        users += [{'user_id': user_id,
                   'group': call.data}]
        
        await call.message.edit_text("Вы зарегистрировались")
        await call.message.answer(f"Ваша группа: {call.data.replace('_', '-')}", reply_markup=await make_menu_keyboard(call.from_user.id))

    await state.finish()

print("registration is import")