from aiogram import Bot, Dispatcher, executor, types

bot = Bot('6322621773:AAHPcJkJwLFS_jpzWWhOJPbMtjiW261huMo')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Здравствуйте посетитель! Рады вас приветствовать вас в нашем магазине. - Hello visitor! We are glad to welcome you to our store.')


@dp.message_handler()
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Site', url='https://www.marwin.kz'))
    markup.add(types.InlineKeyboardButton('Assortment', callback_data='Assortment - Our assortment includes toys for children.'))
    await message.reply('Здравствуйте посетитель! Рады вас приветствовать вас в нашем магазине. - Hello visitor! We are glad to welcome you to our store.', reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


@dp.message_handler(commands=['reply'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Site'))
    markup.add(types.KeyboardButton('Assortment'))
    await message.answer('Здравствуйте посетитель! Рады вас приветствовать вас в нашем магазине. - Hello visitor! We are glad to welcome you to our store.', reply_markup=markup)


executor.start_polling(dp)
