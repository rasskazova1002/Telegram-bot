from telebot import types

info_in_btn = types.KeyboardButton('Информация')
mem_in_btn = types.KeyboardButton('Игра "Тык"')
help_in_btn = types.KeyboardButton('Помощь')
back_in_btn = types.KeyboardButton('<- Назад')
spam_in_btn = types.KeyboardButton('Рассылка')
plans_in_btn = types.KeyboardButton('Расписание')
wants_in_btn = types.KeyboardButton('Хочу в отряд!')


def start_btn(role):
    start_new = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_new.add(info_in_btn, mem_in_btn)
    if role == 1:
        start_new.add(spam_in_btn, plans_in_btn, help_in_btn)
    elif role == 2 or role == 3:
        start_new.add(plans_in_btn, help_in_btn)
    elif role == 0:
        start_new.add(spam_in_btn, wants_in_btn, help_in_btn)
    return start_new


def info_btn():
    info_new = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info_new.add(types.KeyboardButton('РСО'), types.KeyboardButton('Отряды МГУ'),
                 types.KeyboardButton('ПСО "Backspase"'), types.KeyboardButton('<- Назад'))
    return info_new


def rso_btn():
    rso_bttn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rso_bttn.add(types.KeyboardButton('Что такое РСО?'), types.KeyboardButton('География'),
                 types.KeyboardButton('Традиции и ценности РСО'), types.KeyboardButton('<- Назад'))
    return rso_bttn


def otriad_btn():
    otriad_bttn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    otriad_bttn.add(types.KeyboardButton('Какие есть в МГУ?'), types.KeyboardButton('Традиции МСО МГУ'),
                    types.KeyboardButton('История МСО МГУ'), types.KeyboardButton('<- Назад'))
    return otriad_bttn


def pso_btn():
    pso_bttn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    pso_bttn.add(types.KeyboardButton('Что такое ПСО "Backspace"?'), types.KeyboardButton('Девиз отряда'),
                 types.KeyboardButton('Как попасть в отряд?'), types.KeyboardButton('<- Назад'))
    return pso_bttn
