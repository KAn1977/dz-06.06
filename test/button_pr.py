from telebot import types

BUTTON_TEXT = {
    'ru': {
        'send_phone': 'Отправить номер телефона.',
        'send_location': 'Отправить текущую локацию.',
        'my_data': 'Мои личные данные.',
        'show_data': 'Показать личные данные.',
        'edit_data': 'Изменить данные.',
        'back': 'Назад.',
        'change_lang' : "Поменять язык"
    },
    'uz': {
        'send_phone': 'Telefon raqamini yuborish.',
        'send_location': 'Joriy joylashuvni yuborish.',
        'my_data': 'Shaxsiy ma\'lumotlarim.',
        'show_data': 'Shaxsiy ma\'lumotlarni ko\'rsatish.',
        'edit_data': 'Ma\'lumotlarni o\'zgartirish.',
        'back': 'Orqaga.',
        'change_lang' : "Tilni o'zgartirish"
    }
}

"""
Функции для регистрации.
"""
def but_numb(lang):
    pr = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton(BUTTON_TEXT[lang]['send_phone'], request_contact=True)
    pr.add(but1)
    return pr

def but_loc(lang):
    pr = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton(BUTTON_TEXT[lang]['send_location'], request_location=True)
    pr.add(but1)
    return pr


'''
InLine Кнопки
'''
def but_start(lang):
    pr = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(BUTTON_TEXT[lang]['my_data'], callback_data='my_info')

    pr.add(but1)
    return pr

def my_info(lang):
    pr = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(BUTTON_TEXT[lang]['show_data'], callback_data='watch_info')
    but2 = types.InlineKeyboardButton(BUTTON_TEXT[lang]['edit_data'], callback_data='edit_info')
    but4 = types.InlineKeyboardButton(BUTTON_TEXT[lang]['back'], callback_data='back_to_main')
    but3 = types.InlineKeyboardButton(BUTTON_TEXT[lang]['change_lang'], callback_data= 'ch_lang')
    pr.add(but1, but2, but3, but4)
    return pr


def lang():
    pr = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Русский язык.')
    but2 = types.KeyboardButton("O'zbek tili.")
    pr.add(but1, but2)
    return pr
