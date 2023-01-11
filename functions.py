from users import users, admins
from create_bot import bot
"""Модуль, содержащий вспомогательные функции"""

async def is_user(user_id):
    """Функция проверяет, зарегестрирован ли пользователь"""
    for k in users:
        if k['user_id'] == user_id:
            return True
    await bot.send_message(user_id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
    return False

async def is_admin(user_id, group):
    """Функция проверяет, является ли пользователь админом данной группы"""
    for k in range(len(admins)):
        if user_id == admins[k]['user_id']:
            if group == admins[k]['group']:
                return True
            return False

async def take_variable(user_id, variable):
    """Функция берет данные из словаря пользователей по user_id пользователя"""
    for k in users:
        if k['user_id'] == user_id:
            return k[variable]


async def change_variable(user_id, variable, value):
    """Функция изменяет данные из словаря пользователей по user_id пользователя"""
    for k in users:
        if k['user_id'] == user_id:
            k[variable] = value
