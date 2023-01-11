from aiogram.utils import executor

"""Главный модуль"""

# **************TEST********************************
from aiogram.types import Message
from create_data_base import DB
from create_bot import dp

@dp.message_handler(commands=["test"])
async def test(message: Message):
    print("***")
    print("***")


# **************TEST********************************

from handlers import commands
from FSM_modules import registration
from FSM_modules import calendar
from handlers import next_five_deadlines
from FSM_modules import make_admin
from FSM_modules import fsm_other

import notifications

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)