import sqlite3
from telebot import types
import callbacks


def timing(bot, message):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM users WHERE id = {message.chat.id}""")
    datum = cur.fetchall()
    if datum[0][2] == 1:
        bttn = types.InlineKeyboardMarkup()
        bttn.row(types.InlineKeyboardButton('Новое мероприятие', callback_data='timing_new_mero'))
        bttn.row(types.InlineKeyboardButton('Расписание по дате', callback_data='timing_date_mero'))
        bttn.row(types.InlineKeyboardButton('Ближайшее мероприятие', callback_data='timing_close_mero'))
        bot.send_message(message.chat.id, "Вы можете внести в расписание новое мероприятие, а также "
                                          "узнать расписание на конкретную дату и сколько времени осталось "
                                          "до ближайшего мероприятия.", reply_markup=bttn)

    elif datum[0][2] > 1:
        bttn = types.InlineKeyboardMarkup()
        bttn.row(types.InlineKeyboardButton('Расписание по дате', callback_data='timing_date_mero'))
        bttn.row(types.InlineKeyboardButton('Ближайшее мероприятие', callback_data='timing_close_mero'))
        bot.send_message(message.chat.id, 'Вы можете узнать расписание на конкретную дату, а также сколько времени '
                                          'осталось до ближайшего мероприятия.', reply_markup=bttn)

    callbacks.callbacks(bot)
