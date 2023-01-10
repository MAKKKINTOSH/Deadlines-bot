from create_bot import dp
from aiogram.utils import executor

"""Главный модуль"""

from handlers import commands
from FSM_modules import registration
from FSM_modules import calendar
from handlers import next_five_deadlines
from FSM_modules import make_admin
from FSM_modules import fsm_other

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)