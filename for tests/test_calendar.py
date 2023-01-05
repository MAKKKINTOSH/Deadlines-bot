from aiogram import Bot, Dispatcher, types, executor
from TOKEN import Token
from random import randint

bot = Bot(Token)
dp = Dispatcher(bot)

days_array = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31']
callback_for_days = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08', 'd09',
                     'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18',
                     'd19', 'd20', 'd21', 'd22', 'd23', 'd24', 'd25', 'd26', 'd27',
                     'd28', 'd29', 'd30', 'd31']

async def make_start_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Show", "Delete", "Add")
    return kb

async def get_days(month, year):
    quantity_of_days = int
    if month in [1, 3, 5, 6, 8, 10, 12]:
        quantity_of_days = 31
    elif month == 2 and year % 400 == 0:
        quantity_of_days = 29
    elif month == 2 and year % 100 == 0:
        quantity_of_days = 28
    elif month == 2 and year % 4 == 0:
        quantity_of_days = 29
    elif month == 2:
        quantity_of_days = 28
    else:
        quantity_of_days = 30

        return quantity_of_days

async def make_calendar_keyboard(month=1, year=1):
    keyboard=types.InlineKeyboardMarkup(row_width=6)
    b1=types.InlineKeyboardButton("<<", callback_data="<<")
    b2=types.InlineKeyboardButton(">>", callback_data=">>")
    clear_button=types.InlineKeyboardButton(" ", callback_data="clear")
    keyboard.row(b1, b2).add(types.InlineKeyboardButton('0', callback_data='0'))
    size = randint(2, 30)
    print(size)
    for k in range(1, size):
        b=types.InlineKeyboardButton(str(k), callback_data=str(k))
        keyboard.insert(b)

    for k in range(6 - size%6):
        keyboard.insert(clear_button)

    return keyboard


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет", reply_markup= await make_start_keyboard())

@dp.message_handler(regexp='Show')
async def show(message: types.Message):
    await message.answer("show", reply_markup= await make_calendar_keyboard())

@dp.callback_query_handler(text=">>")
async def callbacks(call: types.CallbackQuery):
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.from_user.id,
                                text="show",
                                reply_markup=await make_calendar_keyboard())
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)