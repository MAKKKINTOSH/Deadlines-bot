from create_bot import dp
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

"""В модуле содержатся дополнительные хэндлеры для работы машины состояний"""

@dp.message_handler(content_types="text", state="*")
async def FSM_already_use(message: Message):
    """Функция уведомляет пользователя,
    что он уже использует функцию, связанную с машиной состояний"""

    if message.text in ["Календарь", "Удалить", "Добавить", "Внести админа", "/reg"]:
        await message.answer("Похоже, у вас не закрыто окно регистрации или календарь, "
                             "чтобы продолжить, закройте эти окна")

@dp.callback_query_handler(text="cancel", state="*")
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Действие отменено")
    await call.answer()
    await state.finish()

print("fsm other is import")