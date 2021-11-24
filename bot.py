import telebot
import json
from pathlib import Path

# Подключение файла настроек
from order import create_order

BASE_DIR = Path(__file__).resolve().parent.parent
try:
    with open('config.json') as handle:
        config = json.load(handle)
except IOError:
    config = {
        'token': None,
    }

# Константы
token = config['token']
bot = telebot.TeleBot(token)

print(f"""
    Информация о боте:
Имя бота: @{bot.get_me().username}
токен: {token}
Папка проекта: {BASE_DIR}
©nicstim
    """)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, create_order(message.text, str(message.from_user.id)))


@bot.message_handler(content_types=['text'])
def body(message):
    bot.send_message(message.chat.id, create_order(message.text, str(message.from_user.id)))


bot.skip_pending = True
bot.polling(none_stop=True, interval=0)
