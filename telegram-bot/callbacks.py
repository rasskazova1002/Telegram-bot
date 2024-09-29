import sqlite3
import time
from secret import admin_1
import telebot
from telebot import types
from join_us import deq

logic = 0
last_message_text = ''
last_message_id = 0
downloaded_file = b''
msg_to_change_id = 0


def new_last_message(message):
    global last_message_text
    global last_message_id
    last_message_text = message.text
    last_message_id = message.message_id


def callbacks(bot, msg_to_change_original=None):
    @bot.message_handler(content_types=['photo'])
    def get_photo(message):
        global downloaded_file
        global last_message_id
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            last_message_id = message.message_id

        except Exception as ex:
            bot.reply_to(message, ex)

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_message(callback):
        global msg_to_change_id
        global last_message_text
        global logic
        global downloaded_file
        if msg_to_change_id == 0:
            msg_to_change_id = msg_to_change_original

        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        if callback.data == 'text_spam':
            last_message_text = ''
            counts = 0
            msg_bot = bot.send_message(callback.message.chat.id,
                                       'Введите текст рассылки как можно быстрее, пожалуйста.')
            bot.register_next_step_handler(msg_bot, new_last_message)
            while last_message_text == '' and counts < 5:
                time.sleep(10)
                if last_message_text == '':
                    bot.send_message(callback.message.chat.id, 'Я ЖДУ текст!!! Быстрее, пожалуйста.')
                counts += 1
            if logic == 0:
                bot.edit_message_text(text='Ваш пост: ' + last_message_text,
                                      chat_id=callback.message.chat.id, message_id=msg_to_change_id)
            else:
                bot.delete_message(callback.message.chat.id, msg_to_change_id)
                msg_to_change_id = bot.send_photo(photo=downloaded_file, caption='Ваш пост: ' + last_message_text,
                                                  chat_id=callback.message.chat.id).message_id
            bot.delete_message(callback.message.chat.id, msg_bot.message_id)
            bot.delete_message(callback.message.chat.id, last_message_id)

        elif callback.data == 'photo_spam':
            logic = 1
            downloaded_file = b''
            counts = 0
            msg_bot = bot.send_message(callback.message.chat.id, 'Пожалуйста, пришлите одно изображение.')
            while downloaded_file == b'' and counts < 5:
                time.sleep(10)
                if downloaded_file == b'':
                    bot.send_message(callback.message.chat.id, 'Я ЖДУ фото!!! Быстрее, пожалуйста.')
                counts += 1
            bot.delete_message(callback.message.chat.id, msg_bot.message_id)
            bot.delete_message(callback.message.chat.id, msg_to_change_id)
            bot.delete_message(callback.message.chat.id, last_message_id)
            msg_to_change_id = bot.send_photo(photo=downloaded_file, caption='Ваш пост: ' + last_message_text,
                                              chat_id=callback.message.chat.id).message_id

        elif callback.data == 'for_who':
            btn_for = types.InlineKeyboardMarkup()
            btn0 = types.InlineKeyboardButton('Всем-всем-всем ', callback_data='spam_all')
            btn1 = types.InlineKeyboardButton('Кандидаты', callback_data='spam_kandidats')
            btn2 = types.InlineKeyboardButton('Админы', callback_data='spam_admin')
            btn_for.row(btn0)
            btn_for.row(btn1, btn2)

            bot.send_message(callback.message.chat.id, 'Выберите, кому предназначена рассылка.', reply_markup=btn_for)

        elif callback.data == 'spam_all' or callback.data == 'spam_kandidats' or callback.data == 'spam_admin':
            if callback.data == 'spam_all':
                cur.execute(f"""SELECT * FROM users""")

            elif callback.data == 'spam_kandidats':
                cur.execute(f"""SELECT * FROM users WHERE role = 2""")

            elif callback.data == 'spam_admin':
                cur.execute(f"""SELECT * FROM users WHERE role = 1""")

            if downloaded_file == b'':
                for mess in cur.fetchall():
                    try:
                        bot.send_message(chat_id=mess[0], text=last_message_text)
                    except telebot.apihelper.ApiTelegramException:
                        cur.execute(f"""DELETE FROM users WHERE id = {mess[0]}""")
                        bot.send_message(admin_1(), f'@{mess[1]} больше не с нами...')
            else:
                for mess in cur.fetchall():
                    try:
                        bot.send_photo(chat_id=mess[0], photo=downloaded_file, caption=last_message_text)
                    except telebot.apihelper.ApiTelegramException:
                        cur.execute(f"""DELETE FROM users WHERE id = {mess[0]}""")
                        bot.send_message(admin_1(), f'@{mess[1]} больше не с нами...')

            last_message_text = ''
            downloaded_file = b''

        elif callback.data == 'rassilka_1':
            cur.execute(f"""REPLACE INTO users VALUES ({callback.message.chat.id}, 
                '{callback.message.chat.username}',0)""")
            bot.send_message(callback.message.chat.id, 'Вы подписаны на рассылку!')
        elif callback.data == 'rassilka_0':
            cur.execute(f"""DELETE FROM users WHERE id = {callback.message.chat.id}""")
            bot.send_message(callback.message.chat.id, 'Вы отписались от рассылки!')

        elif callback.data == 'timing_new_mero':
            last_message_text = ''
            counts = 0
            msg_bot = bot.send_message(callback.message.chat.id, 'Чтобы добавить мероприятие, оправьте информацию '
                                                                 'о дате, времени и названии мероприятия в следующем '
                                                                 'формате:\n\n01.01.2035 18:00 Мероприятие для всех\n\n'
                                                                 'Как можно быстрее, пожалуйста.')
            bot.register_next_step_handler(msg_bot, new_last_message)
            while last_message_text == '' and counts < 5:
                time.sleep(10)
                if last_message_text == '':
                    bot.send_message(callback.message.chat.id, 'Я ЖДУ мероприятие!!! Быстрее, пожалуйста.')
                counts += 1
            try:
                cur.execute(f"""INSERT INTO timings VALUES ('{last_message_text[6:10]}-{last_message_text[3:5]}-"""
                            f"""{last_message_text[:2]} {last_message_text[11:16]}', '{last_message_text[17:]}')""")
                bot.send_message(callback.message.chat.id, "Мероприятие успешно добавлено в расписание.")
            except Exception:
                bot.send_message(callback.message.chat.id, 'Ошибка. Данные некорректны или в это '
                                                           'время запланировано другое мероприятие.')

        elif callback.data == 'timing_close_mero':
            cur.execute(f"""DELETE FROM timings WHERE date < CURRENT_TIMESTAMP""")
            cur.execute(f"""SELECT * FROM timings ORDER BY date LIMIT 1""")
            res = cur.fetchall()
            if res:
                bot.send_message(callback.message.chat.id, f'Ближайшее мероприятие: {res[0][1]}, начало {res[0][0]}')
            else:
                bot.send_message(callback.message.chat.id, 'Мероприятий не найдено')
            
        elif callback.data == 'timing_date_mero':
            last_message_text = ''
            counts = 0
            msg_bot = bot.send_message(callback.message.chat.id,
                                       'Чтобы узнать о мероприятиях, оправьте интересующую Вас дату '
                                       'в следующем формате:\n\n01.01.2035\n\n'
                                       'Как можно быстрее, пожалуйста.')
            bot.register_next_step_handler(msg_bot, new_last_message)
            while last_message_text == '' and counts < 5:
                time.sleep(10)
                if last_message_text == '':
                    bot.send_message(callback.message.chat.id, 'Я ЖДУ дату!!! Быстрее, пожалуйста.')
                counts += 1

            cur.execute(f"""SELECT * FROM timings WHERE date LIKE '{last_message_text[6:10]}-
                        {last_message_text[3:5]}-{last_message_text[:2]}%' ORDER BY date""")
            res = ''
            for i in cur.fetchall():
                res += i[0][11:16] + '   ---   ' + i[1] + '\n'
            if res != '':
                bot.send_message(callback.message.chat.id, f'Мероприятия {last_message_text}:\n\n' + res)
            else:
                bot.send_message(callback.message.chat.id, 'Мероприятий на эту дату не найдено.')

        elif callback.data == 'in_backspace_yes':

            if len(deq) > 0:
                markup = types.InlineKeyboardMarkup(row_width=3)
                markup.add(types.InlineKeyboardButton('АДМИН', callback_data='who_admin'),
                           types.InlineKeyboardButton('КАНДИДАТ', callback_data='who_kandidats'),
                           types.InlineKeyboardButton('БОЕЦ', callback_data='who_boets'))
                bot.send_message(admin_1(), f'❗❗❗Кто он??', reply_markup=markup)
            else:
                bot.send_message(admin_1(), 'Очередь пуста')

        elif callback.data == 'in_backspace_no':
            bot.send_message(deq.popleft()[0], 'К сожалению, Ваше членство в отряде не подтверждено')
            bot.send_message(admin_1(), 'Членство в отряде не подтверждено')

        elif callback.data == 'who_admin':
            cur.execute(f"""REPLACE INTO users VALUES({deq[0][0]}, '{deq[0][1]}', 1)""")
            bot.send_message(deq.popleft()[0], 'Ваше членство в отряде подтверждено! Поздравляю!\n'
                                               'Для обновления функционала нажмите /start')

        elif callback.data == 'who_kandidats':
            cur.execute(f"""REPLACE INTO users VALUES({deq[0][0]}, '{deq[0][1]}', 2)""")
            bot.send_message(deq.popleft()[0], 'Ваше членство в отряде подтверждено! Поздравляю!\n'
                                               'Для обновления функционала нажмите /start')
            bot.send_message(admin_1(), 'Членство в отряде подтверждено')

        elif callback.data == 'who_boets':
            cur.execute(f"""REPLACE INTO users VALUES({deq[0][0]}, '{deq[0][1]}', 3)""")
            bot.send_message(deq.popleft()[0], 'Ваше членство в отряде подтверждено! Поздравляю!\n'
                                               'Для обновления функционала нажмите /start')
            bot.send_message(admin_1(), 'Членство в отряде подтверждено')

        conn.commit()
        cur.close()
        conn.close()
