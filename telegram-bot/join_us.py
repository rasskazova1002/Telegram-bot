from secret import admin_2, admin_1
from telebot import types
from collections import deque
import callbacks

deq = deque(maxlen=5)


def join_us(bot, message):
    cur_username = message.chat.username
    cur_user_id = message.chat.id
    if len(deq) == deq.maxlen:
        bot.send_message(cur_user_id, 'Пожалуйста, отправьте запрос позже, очередь переполнена')
    else:
        if (cur_user_id, cur_username) not in deq:
            deq.append((cur_user_id, cur_username))

            bot.send_message(admin_2(), f"Привет! Человек @{cur_username} хочет в отряд, "
                                        f"свяжись с ним, пожалуйста)")

            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton('ДА', callback_data='in_backspace_yes'),
                       types.InlineKeyboardButton('НЕТ', callback_data='in_backspace_no'))
            bot.send_message(admin_1(), f'❗❗❗Человек с ником @{cur_username} хочет вступить в отряд. '
                                        f'Принять заявку?', reply_markup=markup)

            bot.send_message(message.chat.id, 'Я рад твоему интересу 👾 \n\nЧтобы вступить в отряд, должно пройти'
                                              ' некоторое время. \nДля начала предлагаю тебе перейти в беседу новичков '
                                              'всех отрядов МГУ, где будет дальнейшее распределение 🏃‍ 🏃‍♀️‍ 🏃‍♂️‍\n\n'
                                              'А пока я отправлю твои контакты командиру '
                                              'отряда, он постарается связаться с тобой в ближайшее время!')

    callbacks.callbacks(bot)
