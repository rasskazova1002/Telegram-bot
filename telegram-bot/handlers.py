import buttons
import sqlite3
import spam
import timing
import join_us

flag = 0


def role_func(user_id):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM users WHERE id = {user_id}""")
    tmp = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    if len(tmp) > 0:
        return tmp[0][2]
    return 0


def handlers(bot):
    @bot.message_handler()
    def on_click(message):
        global flag
        if message.text == '<- Назад':
            if flag == 0:
                role = role_func(message.chat.id)
                bot.send_message(message.chat.id, 'Пожалуйста, выберите раздел', reply_markup=buttons.start_btn(role))

            elif flag == 1:
                bot.send_message(message.chat.id, 'Пожалуйста, выберите раздел', reply_markup=buttons.info_btn())
                flag = 0
                                                                                        # РАСПИСАНИЕ - БЛОК РАСПИСАНИЕ
        elif message.text == 'Расписание':
            timing.timing(bot, message=message)

                                                                                    # ХОЧУ В ОТРЯД - БЛОК ХОЧУ В ОТРЯД
        elif message.text == 'Хочу в отряд!':
            join_us.join_us(bot, message=message)

                                                                                            # РАССЫЛКА - БЛОК РАССЫЛКА
        elif message.text == 'Рассылка':
            spam.spam_from_kom(bot, message=message)

                                                                                                # ПОМОЩЬ - БЛОК ПОМОЩЬ
        elif message.text == 'Помощь':
            bot.send_message(message.chat.id, 'Всё будет хорошо, обязательно! Главное верь!')

                                                                                        # РАЗВЛЕЧЕНИЯ - БЛОК РАЗВЛЕЧЕНИЯ

        elif message.text == 'Игра "Тык"':
            bot.send_message(message.chat.id, 'Кто скажет "Тык" последним, тот победил.\n\nТык')
        elif message.text.lower() == 'тык':
            bot.send_message(message.chat.id, 'Тык')

                                                                                        # ИНФОРМАЦИЯ - БЛОК ИНФОРМАЦИЯ
        elif message.text == 'Информация':
            bot.send_message(message.chat.id, 'Пожалуйста, выберите раздел', reply_markup=buttons.info_btn())
            flag = 0

        elif message.text == 'РСО':
            bot.send_message(message.chat.id, 'Пожалуйста, выберите раздел', reply_markup=buttons.rso_btn())
            flag = 1
        elif message.text == 'Отряды МГУ':
            bot.send_message(message.chat.id, 'Пожалуйста, выберите раздел', reply_markup=buttons.otriad_btn())
            flag = 1
        elif message.text == 'ПСО "Backspase"':
            bot.send_message(message.chat.id, 'Пожалуйста, выберите раздел', reply_markup=buttons.pso_btn())
            flag = 1
                                                                                                # ТЕКСТОВАЯ ЧАСТЬ РСО
        elif message.text == 'Что такое РСО?':
            bot.send_message(message.chat.id, 'Это Российские студенческие отряды')
        elif message.text == 'География':
            bot.send_message(message.chat.id, 'Ребята из 82 регионов покоряют всю Россию')
        elif message.text == 'Традиции и ценности РСО':
            bot.send_message(message.chat.id, 'Уважение, безопасность, традиции, профессионализм, я = РСО')

                                                                                            # ТЕКСТОВАЯ ЧАСТЬ ОТРЯДЫ МГУ
        elif message.text == 'Какие есть в МГУ?':
            bot.send_message(message.chat.id, 'Педагогические, строительный, сельскохозяйственный, '
                                              'археологический, сервисный, информационный отряды')
        elif message.text == 'Традиции МСО МГУ':
            bot.send_message(message.chat.id, 'Отмечаем масленицу с ректором МГУ')
        elif message.text == 'История МСО МГУ':
            bot.send_message(message.chat.id, 'Возрождение штаба произошло в 2002 г.')

                                                                                            # ТЕКСТОВАЯ ЧАСТЬ BACKSPACE
        elif message.text == 'Что такое ПСО "Backspace"?':
            bot.send_message(message.chat.id, 'Мы молодой студенческий отряд, зарегистрированный в РСО в 2024 г.')
        elif message.text == 'Девиз отряда':
            bot.send_message(message.chat.id, 'Помни о космосе внутри тебя!')
        elif message.text == 'Как попасть в отряд?':
            bot.send_message(message.chat.id, 'Напишите командиру отряда, его контакты есть в нашей группе /vk')
