import secret
import buttons
import handlers

bot = secret.teleb()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую!\nДавайте знакомиться. Я Байтик из студенческого отряда '
                                      '"Backspace" 👾\nМеню находится в нижней части экрана 👇',
                                      reply_markup=buttons.start_btn(role=handlers.role_func(message.chat.id)))

@bot.message_handler(commands=['vk'])
def site(message):
    bot.send_message(message.chat.id, 'Следи за нами Вконтакте:\n\nhttps://vk.com/backspace_msu')


handlers.handlers(bot)

bot.polling(none_stop=True)
