from aiogram import Bot, Dispatcher
from aiohttp import web
from config import Token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

"""Модуль инициализирует бота"""

bot = Bot(Token)
Bot.set_current(bot)

dp = Dispatcher(bot, storage=MemoryStorage())
#application = web.Application()
#
#webhook_path = f'/{Token}'
#
#async def set_webhook():
#    webhook_uri = f"https://1505749-cj90870.tw1.ru{webhook_path}"
#    await bot.set_webhook(webhook_uri)
#
#async def on_startup(_):
#    await set_webhook()
#
#def application_start():
#    global application
#    application.on_startup.append(on_startup)