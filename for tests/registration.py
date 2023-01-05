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

#@dp.message_handler(commands='start')
#async def start(message: types.Message):
#    await message.answer("start", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('1', callback_data='1'),
#                                                                                types.InlineKeyboardButton('2', callback_data='2'),
#                                                                                types.InlineKeyboardButton('3', callback_data='3')))
#
#@dp.callback_query_handler(text=["1","2","3"])
#async def call(call: types.CallbackQuery):
#    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('4', callback_data='4'),
#                                                                                types.InlineKeyboardButton('5', callback_data='5'),
#                                                                                types.InlineKeyboardButton('6', callback_data='6')))
#@dp.callback_query_handler(text=["4", "5", "6"])
#async def call(call: types.CallbackQuery):
#    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('7', callback_data='7'),
#                                                                                types.InlineKeyboardButton('8', callback_data='8'),
#                                                                                types.InlineKeyboardButton('9', callback_data='9')))
#@dp.callback_query_handler(text=["7", "8", "9"])
#async def call(call: types.CallbackQuery):
#    await call.answer(call.data, show_alert=True)
#    await bot.delete_message(call.from_user.id, call.message.message_id)


@dp.message_handler()
async def start(message: types.Message):
    if call.data in ["1", "2", "3"]
    await message.answer("start", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('1', callback_data='1'),
                                                                                types.InlineKeyboardButton('2', callback_data='2'),
                                                                                types.InlineKeyboardButton('3', callback_data='3')))
async def call(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('4', callback_data='4'),
                                                                                types.InlineKeyboardButton('5', callback_data='5'),
                                                                                types.InlineKeyboardButton('6', callback_data='6')))
@dp.callback_query_handler(text=["4", "5", "6"])
async def call(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('7', callback_data='7'),
                                                                                types.InlineKeyboardButton('8', callback_data='8'),
                                                                                types.InlineKeyboardButton('9', callback_data='9')))
@dp.callback_query_handler(text=["7", "8", "9"])
async def call(call: types.CallbackQuery):
    await call.answer(call.data, show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)