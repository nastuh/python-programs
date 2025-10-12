from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo


bot = Bot('')
dp = Dispatcher(bot)


dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://algoritmika.by/ru/1main.py.html')))
    await message.answer('Здравствуйте, рада приветствовать вас на своём чат-боте.', reply_markup=markup)




executor.start_polling(dp)