import sqlite3

con = sqlite3.connect('DB_pr.db', check_same_thread=False)
sql = con.cursor()

# СОЗДАНИЕ ТАБЛИЦЫ
sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, number TEXT, location TEXT, lang TEXT);')

def register(tg_id, name, number, location, lang):
    print(f"Регистрация пользователя: ID={tg_id}, Имя={name}, Номер={number}, Локация={location}, Язык={lang}" )
    sql.execute('INSERT INTO users VALUES (?,?,?,?,?);', (tg_id, name, number, location, lang))
    con.commit()

def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id = ?;', (tg_id,)).fetchone():
        return True
    else:
        return False

def get_user_name(tg_id):
    result = sql.execute('SELECT name FROM users WHERE tg_id = ?;',(tg_id,)).fetchone()
    return result[0] if result else None

def get_user_number(tg_id):
    result = sql.execute('SELECT number FROM users WHERE tg_id = ?;' ,(tg_id,)).fetchone()
    return result[0] if result else None

def all_info(tg_id):
    result = sql.execute('SELECT * FROM users WHERE tg_id = ?;',(tg_id,)).fetchall()
    return result[0] if result else None

def chainge_my_info(tg_id, name, number, location):
    sql.execute('UPDATE users SET name = ?, number = ?, location = ? WHERE tg_id = ?;', (name, number, location, tg_id))
    con.commit()

def change_lang_ru(tg_id):
    new_lang = 'ru'
    sql.execute('UPDATE users SET lang = ? WHERE tg_id = ?;', (new_lang, tg_id))
    con.commit()

def change_lang_uz(tg_id):
    new_lang = 'uz'
    sql.execute('UPDATE users SET lang = ? WHERE tg_id = ?;', (new_lang, tg_id))
    con.commit()

def get_user_lang(tg_id):
    result = sql.execute('SELECT lang FROM users WHERE tg_id = ?;', (tg_id,)).fetchone()
    return result[0] if result else 'ru'