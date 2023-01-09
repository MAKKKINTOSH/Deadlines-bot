from create_bot import dp, DB
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from users import main_admin
from institutes_and_groups import groups_array

"""Модуль для внесения админа через чат с ботом"""

class FSM_admin(StatesGroup):
    take_id = State()
    take_group = State()

cansel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("<<", callback_data="cancel_admin"))

@dp.message_handler(regexp='Внести админа', state=None)
async def add_admin(message: Message, state: FSMContext):
    if message.from_user.id == main_admin:
        async with state.proxy() as storage:
            await message.answer("Введите id")
        await FSM_admin.take_id.set()

@dp.message_handler(content_types=["text"], state=FSM_admin.take_id)
async def take_id(message: Message, state: FSMContext):
    async with state.proxy() as storage:
        storage['id'] = message.text
    await message.answer("Введите группу")
    await FSM_admin.next()

@dp.message_handler(content_types=["text"], state=FSM_admin.take_group)
async def take_group(message: Message, state: FSMContext):
    async with state.proxy() as storage:
        for group in groups_array:
            if group == message.text:
                global admins
                user_id = int(storage['id'])
                await DB.make_admin(user_id, group)

                for i in range(len(admins)):
                    if admins[i]['id'] == user_id:
                        admins.pop(i)
                        break

                admins += [{'id': user_id,
                            'group': group}]

                await message.answer("Админ добавлен")
                return
    await message.answer("Вы неправильно указали группу")
    await state.finish()

@dp.callback_query_handler(text="cancel_admin", state="*")
async def cancel_admin(call: CallbackQuery, state: FSMContext):
    """Отмена добавления админа"""

    await state.finish()
    await call.message.edit_text("Добавление админа отменено")
    await call.answer()