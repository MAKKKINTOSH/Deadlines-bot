from create_bot import dp
from create_data_base import DB
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import cancel_keyboard
from data.users import main_admin, admins
from data.institutes_and_groups import institutes, institutes_callback, courses, groups_array
from FSM_modules.registration import \
    make_registration_keyboard_groups, \
    make_registration_keyboard_courses, \
    make_registration_keyboard_institutes

"""Модуль для внесения админа через чат с ботом"""

class FSM_admin(StatesGroup):
    institute = State()
    course = State()
    group = State()
    take_group = State()
    take_id = State()

#cancel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("<<", callback_data="cancel_admin"))

@dp.message_handler(regexp='Внести админа', state=None)
async def add_admin_query(message: Message):
    """Выбор института"""

    if message.from_user.id == main_admin:
        await message.answer("Выберите институт", reply_markup=await make_registration_keyboard_institutes())
        await FSM_admin.institute.set()

@dp.callback_query_handler(text = list(institutes_callback.values()), state=FSM_admin.institute)
async def chosen_institute(call: CallbackQuery, state: FSMContext):
    """Выбор курса"""

    async with state.proxy() as storage:
        storage['admin_institute'] = institutes[call.data]
        await call.message.edit_text("Выберите курс", reply_markup=await make_registration_keyboard_courses(institutes[call.data]))
        await call.answer()

    await FSM_admin.next()

@dp.callback_query_handler(text = courses, state=FSM_admin.course)
async def chosen_course(call: CallbackQuery, state: FSMContext):
    """Выбор группы"""

    async with state.proxy() as storage:

        await call.message.edit_text("Выберите группу", reply_markup= await make_registration_keyboard_groups(storage['admin_institute'], call.data))
        await call.answer()

    await FSM_admin.next()

@dp.callback_query_handler(text = groups_array, state=FSM_admin.group)
async def chosen_group(call: CallbackQuery, state: FSMContext):
    """Ввод user_id пользователя"""

    async with state.proxy() as storage:
        storage['admin_group'] = call.data
        storage['message_edit_id'] = call.message.message_id
        await call.message.edit_text(f"Группа: {call.data}\n\nВведите user_id пользователя, которого хотите сделать админом", reply_markup=cancel_keyboard)
        await call.answer()

    await FSM_admin.next()

@dp.message_handler(content_types=["text"], state=FSM_admin.take_group)
async def take_id(message: Message, state: FSMContext):
    """Добавления админа в базу данных и массив админов"""

    async with state.proxy() as storage:
        global admins
        try:
            user_id = int(message.text)
        except:
            await message.answer("То что вы ввели, не может быть user_id пользователя\n "
                                 "внесение админа отменено")
            await state.finish()
            return
        user_group = storage["admin_group"]
        await DB.make_admin(user_id, user_group)

        for i in range(len(admins)):
            if admins[i]['user_id'] == user_id:
                admins.pop(i)
                break

        admins += [{'user_id': user_id,
                    'group': user_group}]

        await message.answer(f"Админ добавлен\n"
                             f"Группа: {storage['admin_group']}\n"
                             f"user_id: {user_id}")
        await state.finish()