import sqlite3
from telebot import types
import callbacks

bot_msg_id = 0


def spam_from_kom(bot, message):
    global bot_msg_id
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM users WHERE id = {message.chat.id}""")
    datum = cur.fetchall()
    if len(datum) == 0:
        bttn = types.InlineKeyboardMarkup()
        bttn.add(types.InlineKeyboardButton('Подписаться на рассылку отряда', callback_data='rassilka_1'))
        bot.send_message(message.chat.id, 'Вы можете подписаться на рассылку', reply_markup=bttn)

    elif datum[0][2] == 0:
        bttn = types.InlineKeyboardMarkup()
        bttn.add(types.InlineKeyboardButton('Отписаться от рассылки отряда', callback_data='rassilka_0'))
        bot.send_message(message.chat.id, 'Вы можете отписаться от рассылки', reply_markup=bttn)

    elif datum[0][2] == 1:
        bttn = types.InlineKeyboardMarkup()
        btn0 = types.InlineKeyboardButton('Текст', callback_data='text_spam')
        btn1 = types.InlineKeyboardButton('Фото', callback_data='photo_spam')
        btn2 = types.InlineKeyboardButton('Кому отправляем', callback_data='for_who')
        bttn.row(btn0)
        bttn.row(btn1, btn2)
        bot.send_message(message.chat.id, text='Выберите параметр', reply_markup=bttn)

        msg = bot.send_message(message.chat.id, 'Ваш пост будет показываться здесь')
        bot_msg_id = msg.message_id

    callbacks.callbacks(bot, bot_msg_id)

    conn.commit()
    cur.close()
    conn.close()
