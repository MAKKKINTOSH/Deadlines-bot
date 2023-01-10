from create_bot import dp
from institutes_and_groups import groups_array
from aiogram import types
from keyboards import make_menu_keyboard
from functions import is_user
from users import users, admins

"""В модуле происходит обработка команд, введенных пользователем бота"""

@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    """Команда для начала использования бота"""

    await message.answer("Привет, я - прототип дедлайн бота\n\n"
                         "Чтобы узнать команды, используйте /help\n\n")

    await message.answer("Для того, чтобы пользоваться ботом, выберите группу по команде /reg",
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("/reg")))

@dp.message_handler(commands=['menu'])
async def command_menu(message : types.Message):
    """Команда для вызова главного меню бота"""

    if await is_user(message.from_user.id):
        await message.answer("Выберите действие", reply_markup=await make_menu_keyboard(message.from_user.id))

@dp.message_handler(commands=['contacts'])
async def command_contacts(message : types.Message):
    """Команда для отправки пользователю контактов создателей бота (Я и Саша)"""

    await message.answer("<b><u>Создатели:</u></b>\n\n"
                         "<b><i>Иван</i></b> (Лид) - @Van_Vanskiy\n"
                         "👆по всем вопросам👆\n"
                         "<b><i>Александр</i></b> (Младший научный сотрудник) - @chipul1a", parse_mode="html")


@dp.message_handler(commands=['help'])
async def command_help(message : types.Message):
    """Команда для помощи пользователю"""

    await message.answer("Привет, я - прототип дедлайн бота\n\n"
                         "1./reg - выбор вашей группы)\n"
                         "2./menu - главное меню\n"
                         "3./help - помощь\n"
                         "4./contacts - контакты")
