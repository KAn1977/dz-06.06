import telebot
from telebot import types

bot = telebot.TeleBot('7887526040:AAF4CxYDDdngGp7GK_ujL5Tm6VnEojZNY6g')

# Главное меню с inline-кнопками
def main_menu():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Показать информацию', callback_data='info')
    button2 = types.InlineKeyboardButton('Настройки', callback_data='settings')
    button3 = types.InlineKeyboardButton('Открыть сайт', url='https://example.com')
    markup.add(button1, button2)
    markup.add(button3)
    return markup

# Меню настроек
def settings_menu():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Включить уведомления', callback_data='enable_notifications')
    button2 = types.InlineKeyboardButton('Отключить уведомления', callback_data='disable_notifications')
    button3 = types.InlineKeyboardButton('Назад', callback_data='back_to_main')
    markup.add(button1, button2)
    markup.add(button3)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Добро пожаловать! Выберите действие:', reply_markup=main_menu())

# Обработчик нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'info':
        bot.send_message(call.message.chat.id, 'Это бот с примером использования inline-кнопок.')
    elif call.data == 'settings':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Настройки:', reply_markup=settings_menu())
    elif call.data == 'enable_notifications':
        bot.send_message(call.message.chat.id, 'Уведомления включены.')
    elif call.data == 'disable_notifications':
        bot.send_message(call.message.chat.id, 'Уведомления отключены.')
    elif call.data == 'back_to_main':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Добро пожаловать! Выберите действие:', reply_markup=main_menu())

if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(non_stop=True)