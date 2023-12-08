import sqlite3

connection = sqlite3.connect('SecretSanta.db')

sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, user_name TEXT, '
            'which_class INTEGER, desc_user TEXT, present_to TEXT, creator BOOLEAN);')

sql.execute('CREATE TABLE IF NOT EXISTS classes (id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, class_name TEXT,'
            'description TEXT, gift_amount TEXT DEFAULT NULL, date DATE, token TEXT);')

connection.commit()

connection.close()


def register_user(tg_id, name, user_name, which_class, desc_user, present_to, creator):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    sql_lite.execute('INSERT INTO users (tg_id, name, user_name, which_class, desc_user, present_to, creator) VALUES '
                     '(?,?,?,?,?,?,?);',
                     (tg_id, name, user_name, which_class, desc_user, present_to, creator))

    db.commit()

    db.close()


def register_class(tg_id, class_name, description, gift_amount, date, token):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    sql_lite.execute('INSERT INTO classes (tg_id, class_name, description, gift_amount, date, token) VALUES '
                     '(?,?,?,?,?,?);',
                     (tg_id, class_name, description, gift_amount, date, token))

    db.commit()

    db.close()


def check_token_class(clas, token):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    result = sql_lite.execute('SELECT * FROM classes WHERE class_name=? AND token=?;', (clas, token)).fetchone()

    if result:
        return result
    else:
        return False


def checker_creator(tg_id):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    result = sql_lite.execute('SELECT creator FROM users WHERE tg_id=?;', (tg_id,)).fetchone()

    if result:
        info_class = sql_lite.execute('SELECT * FROM classes WHERE tg_id=?;', (tg_id,)).fetchone()
        return info_class
    else:
        return False


def check_user_class(tg_id):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    info_user = sql_lite.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone()

    if info_user:
        id_clas = info_user[3]
        info_class = sql_lite.execute('SELECT * FROM classes WHERE id=?;', (id_clas,)).fetchone()
        return info_class + info_user

    else:
        return False


def checker(tg_id):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    result = sql_lite.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone()

    db.close()

    if result:
        return result
    else:
        return False


def get_clas_people_db(clas_id):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    result = sql_lite.execute('SELECT name FROM users WHERE which_class=?;', (clas_id,)).fetchall()

    if result:
        return result
    else:
        return False


def get_all_classes():
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    result = sql_lite.execute('SELECT class_name FROM classes;').fetchall()

    if result:
        return result
    else:
        pass


def del_user_db(tg_id):
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    sql_lite.execute('DELETE FROM users WHERE tg_id=?;', (tg_id,))

    db.commit()


def get_all_tokens_db():
    db = sqlite3.connect('SecretSanta.db')

    sql_lite = db.cursor()

    result = sql_lite.execute('SELECT token FROM classes;').fetchall()

    return result
