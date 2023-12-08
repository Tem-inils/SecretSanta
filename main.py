import time
import telebot
from telebot.types import ReplyKeyboardRemove

from models import checker, register_class, register_user, checker_creator, check_user_class, \
    del_user_db, check_token_class
from buttons import choice_class, get_clas_people_btn
from service import generate_token, get_all_class_service

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id

    check = checker(user_id)

    if check:
        check2 = checker_creator(user_id)
        if check2:
            bot.send_message(user_id, f'{check[1]}  Хо-Хо-Хо, Кого я вижу в наших зимних краях ❄')
            bot.send_message(user_id, f'Название класса - {check2[2]}\n'
                                      f'Условия класса - \n{check2[3]}\n'
                                      f'Минимальная ставка - {check2[4]}\n'
                                      f'Дата окончания ивента - {check2[5]}\n'
                                      f'Уникальный токен класса - {check2[6]}\n')
        else:
            check3 = check_user_class(user_id)
            if check3:
                print(check3)
                bot.send_message(user_id, f'ВАША ИНФОРМАЦИЯ \n\n'
                                          f'Ваш псевдоним - {check3[8]}\n'
                                          f'Ваш юзер - @{check3[9]}\n'
                                          f'Ваше пожелание - \n{check3[11]}\n'
                                          f'Кому вы дарите - {check3[12]}\n\n'
                                          f'ИНФОРМАЦИЯ О КЛАССЕ\n\n'
                                          f'Имя класса - {check3[2]}\n'
                                          f'Правила - \n{check3[3]}\n'
                                          f'Минимальная ставка - {check3[4]}\n'
                                          f'Дата окончания Event - {check3[5]}\n')
            else:
                bot.register_next_step_handler(message, del_user)
    else:
        bot.send_message(user_id, '*Добро пожаловать на Event SECRET SANTA* 🎅🤶\n\n'
                                  '✨ Давай пройдем минимальную регистрацию =) ✨', parse_mode="Markdown")
        bot.send_message(user_id, '✨Сейчас мой маленький Санта 🎅🤶 тебе надо написать свое имя ✨\n'
                                  '*❗Важно знать❗️*\n'
                                  'Соблюдайте регистр *АЛЬБЕРТ* и *альберт* или *Альберт* это все разные имена\n'
                                  'Не правильная запись может превести к ошибкам !\n'
                                  'Правильно: (Альберт)', parse_mode="Markdown")
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(conntent_type=['text'])
def get_name(message):
    user_id = message.from_user.id

    if message.text:
        name = message.text
        bot.send_message(user_id,
                         'Хо-Хо-Хо Ооооотлично🎅\nТеперь тебе надо определистся с выборм класса или создать свой !',
                         reply_markup=choice_class())
        bot.register_next_step_handler(message, get_clas, name)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def get_clas(message, name):
    user_id = message.from_user.id
    # Получаем все классы
    all_clsc = get_all_class_service()

    if message.text == 'Создать класс 😁':
        bot.send_message(user_id, 'Добро пожаловать в ряды не получающих подарки 🎅\n'
                                  'Либо командуй либо подчиняйся, и так твоя задача:\n'
                                  '1️⃣ Написать название и номер класса\n'
                                  '❗ Пример:(11А)', reply_markup=ReplyKeyboardRemove())

        bot.register_next_step_handler(message, get_description, name)
    elif message.text in all_clsc:
        # Получаем название класса
        class_name = message.text

        bot.send_message(user_id, 'Отлично теперь введи уникальный токен класса\n'
                                  'Этот уникальный токен можно попросить у создателя класса!',
                         reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, check_token, name, class_name)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def check_token(message, name, clas_name):
    user_id = message.from_user.id

    if message.text:
        user_token = message.text

        result = check_token_class(clas_name, user_token)

        if result:
            bot.send_message(user_id, 'Отлично теперь напиши свое пожелание')
            bot.register_next_step_handler(message, get_desc_user, name, result[0])
        else:
            bot.send_message(user_id, 'Проблеы с токеном обратись к создателью класса !')
            bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def get_desc_user(message, name, id_clas):
    user_id = message.from_user.id

    if message.text:
        desc_user = message.text

        bot.send_message(user_id, 'Отлично теперь напиши кому ты будешь делать подарок или\n'
                                  'выбери этого человека из кнопочек если он там есть\n'
                                  'Пример: (Альберт)', reply_markup=get_clas_people_btn(id_clas))

        bot.register_next_step_handler(message, get_gift_to_user, name, id_clas, desc_user)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def get_gift_to_user(message, name, id_clas, desc_user):
    user_id = message.from_user.id
    user_name = message.from_user.username

    if message.text:
        get_to = message.text
        register_user(tg_id=user_id, name=name, user_name=user_name, which_class=id_clas, desc_user=desc_user,
                      present_to=get_to, creator=False)
        bot.send_message(user_id, 'Поздровляю на этом все тыкай /start', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def get_description(message, name):
    user_id = message.from_user.id

    if message.text:
        clas_name = message.text

        bot.send_message(user_id, '✨Теперь придумай минимальное описание на свой выбор✨\n'
                                  '❗ Пример:\n '
                                  'Правила игры:\n'
                                  '1️⃣ Не рассказывать о игре =)\n'
                                  '2️⃣ Не отклоняться от общей суммовой ставки =)\n'
                                  '3️⃣ Не дарить деньги и Т.Д...')
        bot.register_next_step_handler(message, get_gift_amount, name, clas_name)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def get_gift_amount(message, name, clas_name):
    user_id = message.from_user.id

    if message.text:
        clas_description = message.text

        bot.send_message(user_id, '✨ Теперь давай выберем минимальную ставку для каждого подарка ✨')
        bot.register_next_step_handler(message, get_date, name, clas_name, clas_description)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def get_date(message, name, clas_name, clas_description):
    user_id = message.from_user.id

    if message.text:
        clas_gift = message.text

        bot.send_message(user_id, '✨ Теперь давай выберем дату окончания вашего Event ✨')
        bot.register_next_step_handler(message, fineshed, name, clas_name, clas_description,
                                       clas_gift)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def fineshed(message, name, clas_name, clas_description, clas_gift):
    user_id = message.from_user.id
    use_name = message.from_user.username

    if message.text:
        clas_date = message.text

        register_user(tg_id=user_id, name=name, user_name=use_name,
                      which_class=None, desc_user=None, present_to=None, creator=True)

        get_token = generate_token()
        bot.send_message(user_id, 'Поздравляю класс и Event создан а ты его создатель !\n'
                                  f'Вот уникальный токен он нужен для входа участникам\n'
                                  f'TOKEN - ```\n{get_token}\n```'
                                  f'тыкай /start', parse_mode='Markdown')
        register_class(tg_id=user_id, class_name=clas_name, description=clas_description,
                       gift_amount=clas_gift, date=clas_date, token=get_token)
        bot.register_next_step_handler(message, start_message)
    else:
        bot.send_message(user_id, 'ERROR BOT...Please Wait 5 Seconds ➕➖')
        time.sleep(3)
        bot.delete_message(user_id, message.message_id)
        bot.register_next_step_handler(message, start_message)


def del_user(message):
    user_id = message.from_user.id

    del_user_db(user_id)

    bot.send_message(user_id, 'Произошли технические шоколадки пройдите регистрацию заново !',
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, start_message)


bot.polling(none_stop=True)
