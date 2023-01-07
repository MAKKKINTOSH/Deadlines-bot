from create_bot import dp
from aiogram.types import Message, CallbackQuery

"""Модуль для регистрации колбеков инлайн клавиатуры"""

@dp.callback_query_handler(text='cancel')
async def cancel(call : CallbackQuery):
    ""