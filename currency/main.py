import telebot
from currency_converter import CurrencyConverter
from telebot import types


bot = telebot.TeleBot('your_bot_token')
currency = CurrencyConverter()
amount = 0



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите сумму которую хотите перевести: - Hello! Enter the amount you want to transfer:')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Напишите сумму! - Wrong format. Write the amount!')
        bot.register_next_step_handler(message, summa)
        return


    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('RUB/BYN', callback_data='rub/byn')
        btn4 = types.InlineKeyboardButton('BYN/RUB', callback_data='byn/rub')
        btn5 = types.InlineKeyboardButton('USD/BYN', callback_data='usd/byn')
        btn6 = types.InlineKeyboardButton('BYN/USD', callback_data='byn/usd')
        btn7 = types.InlineKeyboardButton('KZT/BYN', callback_data='kzt/byn')
        btn8 = types.InlineKeyboardButton('BYN/KZT', callback_data='byn/kzt')
        btn9 = types.InlineKeyboardButton('IDR/BYN', callback_data='idr/byn')
        btn10 = types.InlineKeyboardButton('BYN/IDR', callback_data='byn/idr')
        btn11 = types.InlineKeyboardButton('Другое значение - Other meaning', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
        bot.send_message(message.chat.id, 'Выберите любую пару валют - Choose any pair of currencies', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше чем 0. Введите сумму больше 0. - The number must be greater than 0. Enter an amount greater than 0.')
        bot.register_next_step_handler(message, summa)



@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается - It turns out: {round(res, 2)}. Можете заново вписать сумму. - You can re-enter the amount.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэщ. - Enter a pair of values through a slash.')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.rext.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается - It turns out: {round(res, 2)}. Можете заново вписать сумму. - You can re-enter the amount.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так. Впишите значение заново.')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)