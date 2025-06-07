import requests
import json
import telebot
from jinja2.lexer import operator_re

bot = telebot.TeleBot('7608726159:AAHva-X6_958kg7G48wwyW9KMjXxP9nE4Yg')
API = '72196223258f38a1815fa80718c2ef25'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши мне название города и я пришлю сводку погоды!")

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city =message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.reply_to(message, f'Сейчас погода: {temp}')


        image = 'sun.png' if  temp > 5.0 else 'asd.jpg'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан неверно.')


bot.polling(none_stop=True)
