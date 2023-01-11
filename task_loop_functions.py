from create_data_base import DB
from institutes_and_groups import groups_array
from create_bot import bot
from users import users
from datetime import datetime
from date_variables import current_year, current_month
from asyncio import sleep

"""Модуль содержит в себе, функции, выполняющиеся в цикле событий"""

async def deadlines_notification(wait_for):
    """Отправка уведомлений о приближающихся дедлайнах"""

    day = 9

    while(True):
        if day != datetime.now().day:
            day = datetime.now().day
            for n in [1, 7]:
                for group in groups_array:
                    text = await DB.deadlines_notification(group, n)
                    if text:
                        for user in users:
                            if user['group'] == group:
                                await bot.send_message(user['id'], text)

        await sleep(wait_for)

async def change_current_date(wait_for):
    """Изменяет переменные с текущим годом и месяцем"""

    while(True):
        current_year = datetime.now().year
        current_month = datetime.now().month
        await sleep(wait_for)