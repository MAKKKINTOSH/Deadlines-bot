from create_bot import dp
from aiogram.types import Message

@dp.message_handler(content_types=['text'], state="*")
async def FSM_already_use(message: Message):
    """Функция уведомляет пользователя,
    что он уже использует функцию, связанную с машиной состояний"""

    await message.answer("Похоже, у вас не закрыто окно регистрации или календарь, "
                         "бот, к сожалению, не совершенен, "
                         "так что чтобы продолжить, закройте эти окна")