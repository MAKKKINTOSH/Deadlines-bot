from create_bot import dp
from aiogram.utils import executor

"""Главный модуль"""

from handlers import registration
from handlers import commands
from handlers import text

# не все хэндлеры импортированы

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)