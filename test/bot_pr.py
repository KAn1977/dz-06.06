import telebot
import button_pr
import database_pr
import lang_pr



bot = telebot.TeleBot('7887526040:AAF4CxYDDdngGp7GK_ujL5Tm6VnEojZNY6g')
user_lang = {}

TEXT = {
    'ru': {
        'start_reg': 'Приветствую, давайте начнем регистрацию. Введите свое имя.',
        'enter_phone': 'Отлично! Теперь нужен ваш номер телефона.',
        'send_location': 'Вы просто гений! Осталось получить вашу локацию.',
        'use_phone_button': 'Отправьте номер через кнопку для продолжения регистрации.',
        'use_location_button': 'Отправьте локацию через кнопку для завершения регистрации.',
        'reg_success': 'Регистрация прошла успешно.',
        'choose_lang': 'Выберите язык / Tilni tanlang',
        'hello' : 'Добро пожаловать в бот для практики.',
        'edit_name': 'Введите новое имя:',
        'edit_phone': 'Введите новый номер телефона:',
        'edit_location': 'Отправьте новую локацию через кнопку.',
        'edit_location_error': 'Отправьте локацию через кнопку для завершения изменения данных.',
        'my_data': 'Мои данные.',
        'back_to_menu': 'Вы вернулись в главное меню.',
        'user_data': 'Данные пользователя',
        'lang_is_ch' : 'Язык изменился на русский.'
    },
    'uz': {
        'start_reg': 'Assalomu alaykum, roʻyxatdan oʻtishni boshlaylik. Ismingizni kiriting.',
        'enter_phone': 'Ajoyib! Endi telefon raqamingiz kerak.',
        'send_location': 'Rahmat! Endi joylashuvingizni yuboring.',
        'use_phone_button': 'Roʻyxatdan oʻtishni davom ettirish uchun raqamni tugma orqali yuboring.',
        'use_location_button': 'Roʻyxatdan oʻtishni yakunlash uchun joylashuvni tugma orqali yuboring.',
        'reg_success': 'Roʻyxatdan oʻtish muvaffaqiyatli yakunlandi.',
        'choose_lang': 'Выберите язык / Tilni tanlang',
        'hello' :'amaliyot botiga xush kelibsiz.',
        'edit_name': 'Yangi ismingizni kiriting:',
        'edit_phone': 'Yangi telefon raqamingizni kiriting:',
        'edit_location': 'Yangi joylashuvni tugma orqali yuboring.',
        'edit_location_error': 'Ma\'lumotlarni o\'zgartirish uchun joylashuvni tugma orqali yuboring.',
        'my_data': 'Mening ma\'lumotlarim.',
        'back_to_menu': 'Asosiy menyuga qaytdingiz.',
        'user_data': 'Foydalanuvchi ma\'lumotlari',
        'lang_is_ch' : 'Til o‘zbekchaga o‘zgardi.'
    }}

# /start (РЕГИСТРАЦИЯ)
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if database_pr.check_user(user_id):
        user_name = database_pr.get_user_name(user_id)
        user_lang[user_id] = database_pr.get_user_lang(user_id)
        bot.send_message(user_id, f"{TEXT[user_lang[user_id]]['hello']}, {user_name}",
                         reply_markup=button_pr.but_start(user_lang[user_id]))
    else:
        bot.send_message(user_id, TEXT['ru']['choose_lang'], reply_markup=button_pr.lang())
        bot.register_next_step_handler(message, Text)

@bot.message_handler(content_types=['text'])
def Text(message):
    user_id = message.from_user.id
    text = message.text
    if text == 'Русский язык.':
        user_lang[user_id] = 'ru'
        bot.send_message(user_id, TEXT['ru']['start_reg'], reply_markup= telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)
    elif text == "O'zbek tili.":
        user_lang[user_id] = 'uz'
        bot.send_message(user_id, TEXT['uz']['start_reg'], reply_markup= telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    lang = user_lang[user_id]
    bot.send_message(user_id, TEXT[lang]['enter_phone'], reply_markup=button_pr.but_numb(lang))
    bot.register_next_step_handler(message, get_numb, user_name)


def get_numb(message, user_name):
    user_id = message.from_user.id
    lang = user_lang[user_id]
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, TEXT[lang]['send_location'],
                         reply_markup=button_pr.but_loc(lang))
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    else:
        bot.send_message(user_id, TEXT[lang]['use_phone_button'],
                         reply_markup=button_pr.but_numb(lang))
        bot.register_next_step_handler(message, get_numb, user_name)


def get_loc(message, user_name, user_num):
    user_id = message.from_user.id
    lang = user_lang[user_id]
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        user_loc = f'{latitude}, {longitude}'
        database_pr.register(user_id, user_name, user_num, user_loc, lang)
        bot.send_message(user_id, TEXT[lang]['reg_success'], reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, f"{TEXT[lang]['hello']}, {user_name}",
                         reply_markup=button_pr.but_start(lang))
    else:
        bot.send_message(user_id, TEXT[lang]['use_location_button'],
                         reply_markup=button_pr.but_loc(lang))
        bot.register_next_step_handler(message, get_loc, user_name, user_num)


# Декоратор inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def call_back_inline(call):
    user_id = call.message.chat.id
    lang = user_lang[user_id]

    if call.data == 'my_info':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=TEXT[lang]['my_data'], reply_markup=button_pr.my_info(lang))
    elif call.data == 'watch_info':
        user_name = database_pr.get_user_name(user_id)
        user_info = database_pr.all_info(user_id)
        bot.send_message(chat_id=user_id,text=f"{TEXT[lang]['user_data']} {user_name}:\n{user_info}")
    elif call.data == 'back_to_main':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=TEXT[lang]['back_to_menu'],reply_markup=button_pr.but_start(lang))
    elif call.data == 'edit_info':
        bot.send_message(call.message.chat.id, TEXT[lang]['edit_name'])
        bot.register_next_step_handler(call.message, edit_name)
    elif call.data =='ch_lang':
        user_name = database_pr.get_user_name(user_id)
        if user_lang[user_id] == 'ru':
            user_lang[user_id] = 'uz'
            database_pr.change_lang_uz(user_id)  # Исправлено: вызываем правильную функцию
            # Используем новый язык для текста
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=TEXT['uz']['lang_is_ch'], reply_markup=button_pr.my_info('uz'))

        elif user_lang[user_id] == 'uz':
            user_lang[user_id] = 'ru'
            database_pr.change_lang_ru(user_id)  # Исправлено: вызываем правильную функцию
            # Используем новый язык для текста
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=TEXT['ru']['lang_is_ch'], reply_markup=button_pr.my_info('ru'))





def edit_name(message):
    user_id = message.from_user.id
    lang = user_lang[user_id]
    new_name = message.text
    bot.send_message(user_id, TEXT[lang]['edit_phone'])
    bot.register_next_step_handler(message, edit_number, new_name)


def edit_number(message, new_name):
    user_id = message.from_user.id
    lang = user_lang[user_id]
    new_number = message.text
    bot.send_message(user_id, TEXT[lang]['edit_location'], reply_markup=button_pr.but_loc(lang))
    bot.register_next_step_handler(message, edit_location, new_name, new_number)


def edit_location(message, new_name, new_number):
    user_id = message.from_user.id
    lang = user_lang[user_id]
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        new_location = f'{latitude}, {longitude}'
        database_pr.chainge_my_info(user_id, new_name, new_number, new_location)
        bot.send_message(user_id, TEXT[lang]['reg_success'], reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, f"{TEXT[lang]['hello']}, {new_name}",
                         reply_markup=button_pr.but_start(lang))
    else:
        bot.send_message(user_id, TEXT[lang]['edit_location_error'],
                         reply_markup=button_pr.but_loc(lang))
        bot.register_next_step_handler(message, edit_location, new_name, new_number)


if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(non_stop=True)
