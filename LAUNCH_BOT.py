from create_bot import dp
from aiogram.utils import executor

"""Главный модуль"""

from handlers import commands
from FSM_modules import registration
from FSM_modules import edit_calendar
from handlers import text
from handlers import common_callbacks
from FSM_modules import make_admin

# не все хэндлеры импортированы

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)