from aiogram.utils import executor
from asyncio import get_event_loop
from create_bot import dp

"""Главный модуль"""

from handlers import commands
from FSM_modules import registration
from FSM_modules import calendar
from handlers import next_five_deadlines
from FSM_modules import make_admin
from FSM_modules import fsm_other

from task_loop_functions import deadlines_notification, change_current_date

if __name__ == "__main__":

    from data import institutes_and_groups

    from create_data_base import DB

    print("Congrats, bot is actually working!!!")

    loop = get_event_loop()
    loop.create_task(deadlines_notification(60*60*3))
    loop.create_task(change_current_date(60*60*6))
    executor.start_polling(dp, skip_updates=True)