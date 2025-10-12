import telebot
import requests
import json


bot = telebot.TeleBot('your_bot_token')
API = 'api'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Впиши пожалуйста город, в котором ты хотел бы узнать погоду. - Hello! Please enter the city where you would like to know the weather.')



@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = json.loads(res.text)
    temp = data["main"]["temp"]
    bot.reply_to(message,f'На данный момент погода в выбранном месте составляет: - At the moment, the weather in the selected location is: {temp}')

    image = 'sun.png' if temp > 10.0 else 'bubbles.png'
    file = open('./' + image, 'rb')
    bot.send_photo(message.chat.id, file)

bot.polling(none_stop=True)