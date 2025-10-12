from aiogram import Bot, Dispatcher, executor, types


bot = Bot('')
dp = Dispatcher(bot)


@dp.message_handler(content_types=['photo'])
async def start(message: types.Message):
    await message.reply('Здравствуйте посетитель! Рады вас приветствовать вас в нашем магазине. - Hello visitor! We are glad to welcome you to our store.')


@dp.message_handler()
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Site', url='https://www.marwin.kz'))
    markup.add(types.InlineKeyboardButton('Assortment', callback_data='В наш ассортимент входят игрушки для детей разных возрастов, и многое другое для наших маленьких и не только покупателей. - Our assortment includes toys for children of different ages, and much more for our little and not only customers'))
    await message.reply('Здравствуйте посетитель! Рады вас приветствовать вас в нашем магазине. - Hello visitor! We are glad to welcome you to our store.', reply_markup=markup)



@dp.callback_query_handler(commands=['inline'])
async def callback(call):
    await call.message.aswer(call.data)


@dp.message_handler(commands=['reply'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Site'))
    markup.add(types.KeyboardButton('Assortment'))
    await message.answer('Здравствуйте посетитель! Рады вас приветствовать вас в нашем магазине. - Hello visitor! We are glad to welcome you to our store.', reply_markup=markup)


executor.start_polling(dp)