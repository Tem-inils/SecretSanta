from telebot import types
from models import get_all_classes, checker_creator, get_clas_people_db


# 302137006
def choice_class():
    buttons = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = types.KeyboardButton('Создать класс 😁')
    buttons.row(btn1)

    try:
        all_clss = get_all_classes()
        print(f'buttons - {all_clss}')

        for class_name in all_clss:
            class_button = types.KeyboardButton(str(class_name).strip("(),'"))

            buttons.add(class_button)

    except Exception as e:
        print(f'Exception - {str(e)}')
        pass

    return buttons


def get_clas_people_btn(clas_id):
    buttons = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    try:
        people = get_clas_people_db(clas_id)
        print(f'people - {people}')
        for i in people:
            btn = types.KeyboardButton(str(i).strip("(),'"))

            buttons.add(btn)
    except Exception as e:
        print(f'Exception - {str(e)}')

        btn1 = types.KeyboardButton('Людей пока что нету, не тыкай пиши')
        buttons.add(btn1)

    return buttons
