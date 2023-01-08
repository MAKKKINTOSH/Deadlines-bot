from create_bot import dp, DB
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from functions import is_user, is_admin, take_variable
from config import callback_for_days


"""Модуль для удаления и внесения дедлайнов через календарь"""

class FSM_add(StatesGroup):
    add_deadline = State()

class FSM_delete(StatesGroup):
    delete_deadline = State()


c