import logging

from aiogram.utils import executor
from asyncio import get_event_loop
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import config
from create_bot import dp, bot

"""Главный модуль"""

logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

async def on_startup(dp):
    await bot.set_webhook(config.webhook_url)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

#BOT BODY
from handlers import commands
from FSM_modules import registration
from FSM_modules import calendar
from handlers import text_commands
from FSM_modules import make_admin
from FSM_modules import fsm_other
#/BOT BODY

from task_loop_functions import deadlines_notification, change_current_date

if __name__ == "__main__":
    from data import institutes_and_groups

    from create_data_base import DB

    DB.create_group_tables()

    print("data base is init!")

    loop = get_event_loop()
    loop.create_task(deadlines_notification(60 * 60 * 3))
    loop.create_task(change_current_date(60 * 60 * 6))

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.webapp_host,
        port=config.webapp_port
    )

    print("Congrats, bot is actually working!!!")
