from config import users, admins
from create_bot import bot
"""Модуль, содержащий вспомогательные функции"""

async def is_user(id):
    """Функция проверяет, зарегестрирован ли пользователь"""
    for k in users:
        if k['id'] == id:
            return True
    await bot.send_message(id, "Вы не выбрали группу\n\nВыбрать группу можно по команде /reg")
    return False

async def is_admin(id, group):
    """Функция проверяет, является ли пользователь админом данной группы"""
    for k in range(len(admins)):
        if id == admins[k]['id']:
            if group == admins[k]['group']:
                return True
            return False

async def take_variable(id, variable):
    """Функция берет данные из словаря пользователей по id пользователя"""
    for k in users:
        if k['id'] == id:
            return k[variable]


async def change_variable(id, variable, value):
    """Функция изменяет данные из словаря пользователей по id пользователя"""
    for k in users:
        if k['id'] == id:
            k[variable] = value