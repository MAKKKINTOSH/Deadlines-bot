from create_bot import dp
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from institutes_and_groups import registration_dictionary, institutes, courses, groups_array
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import  State, StatesGroup
from datetime import datetime

"""Модуль для регистрации пользователя"""

class FSM_registration(StatesGroup):
    institute = State()
    course = State()
    group = State()

async def make_registration_keyboard_institutes():
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    kb.add(InlineKeyboardButton("<<", callback_data="cancel_reg"))
    return kb

async def make_registration_keyboard_courses(institute):
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary[institute]:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    kb.add(InlineKeyboardButton("<<", callback_data="cancel_reg"))
    return kb

async def make_registration_keyboard_groups(institute, course):
    kb = InlineKeyboardMarkup()
    for k in registration_dictionary[institute][course]:
        kb.add(InlineKeyboardButton(k, callback_data=k))
    kb.add(InlineKeyboardButton("<<", callback_data="cancel_reg"))
    return kb

@dp.message_handler(commands = ['reg'], state=None)
async def command_registration(message: Message):
    """Команда для выбора группы студента"""

    await FSM_registration.institute.set()
    await message.answer("Выберите институт", reply_markup=await make_registration_keyboard_institutes())
    print(message.from_user.id, datetime.now().hour, datetime.now().minute)

@dp.callback_query_handler(text = institutes, state=FSM_registration.institute)
async def chosen_institute(call: CallbackQuery, state: FSMContext):
    """Выбор курса"""

    async with state.proxy() as storage:
        storage['institute'] = call.data
    await FSM_registration.next()
    await call.message.edit_text("Выберите курс", reply_markup= await make_registration_keyboard_courses(call.data))
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

    async with state.proxy() as storage:
        await call.answer(f"{storage['institute']} {storage['course']} {call.data}", show_alert=True)
        await call.message.edit_text("Вы успешно выбрали группу")
    await state.finish()

@dp.callback_query_handler(text="cancel_reg", state='*')
async def cancel_registration(call: CallbackQuery, state: FSMContext):
    """Отмена регистрации"""

    await state.finish()
    await call.message.edit_text("Регистрация отменена")

@dp.message_handler(commands = ['reg'], state="*")
async def already_registration(message: Message):
    """Защита от одновременной регистрации"""

    await message.answer("Похоже, вы уже начали регистрацию")
