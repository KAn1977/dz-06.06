import telebot
import button_pr
import database_pr


bot = telebot.TeleBot('7887526040:AAF4CxYDDdngGp7GK_ujL5Tm6VnEojZNY6g')
def regist(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Приветствую, давайте начнем регистрацию. Введите свое имя.',
                     reply_markup=telebot.types.ReplyKeyboardMarkup())
    bot.register_next_step_handler(message, get_name)


    def get_name(message):
        user_id = message.from_user.id
        user_name = message.text
        bot.send_message(user_id, 'Отлично! Теперь нужен ваш номер телефона.',reply_markup=button_pr.but_numb())
        bot.register_next_step_handler(message, get_numb, user_name)


    def get_numb(message, user_name):
        user_id = message.from_user.id
        if message.contact:
            user_num = message.contact.phone_number
            bot.send_message(user_id, ', вы просто гений ! осталось получить вашу локацию.',
                             reply_markup=button_pr.but_loc())
            bot.register_next_step_handler(message, get_loc, user_name, user_num)
        else:
            bot.send_message(user_id, 'Отправьте номер через кнопку для продолжения регистрации.',
                             reply_markup=button_pr.but_numb())
            bot.register_next_step_handler(message, get_numb, user_name)


    def get_loc(message, user_name, user_num):
        user_id = message.from_user.id
        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude
            user_loc = f'{latitude}, {longitude}'
            database_pr.register(user_id, user_name, user_num, user_loc)
            bot.send_message(user_id, f'Регистрация прошла успешно.', reply_markup=button_pr.but_start())
        else:
            bot.send_message(user_id, 'Отправьте локацию через кнопку для завершения регистрации.',
                            reply_markup=button_pr.but_loc())
            bot.register_next_step_handler(message, get_loc, user_name, user_num)

