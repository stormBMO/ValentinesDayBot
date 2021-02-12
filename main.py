# coding=utf-8
import telebot

# ----------------------------------------------------------------------------
token_bot = '1654475418:AAHZ8MOBnHgH2t66qL4jvSbsrUqrFymufF8'
bot = telebot.TeleBot(token_bot)
flag_for_schedule = 0
keyboard_hider = telebot.types.ReplyKeyboardRemove()
# ----------------------------------------------------------------------------

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "/start" :
        markup = generate_start_markup() 
        bot.send_message(message.chat.id, "Привет! Это бот для валентинок (не знаю, придумайте сюда текст - я вставлю). Чтобы отправить валентинку, нажми кнопку ниже", reply_markup=markup)

    elif message.text == "Отправить валентинку":
        bot.send_message(message.chat.id, "Сначала отпаравь мне саму валентинку, затем напиши кому ее отправить",reply_markup=keyboard_hider)


def generate_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Отправить валентинку')
    markup.row(button1)
    return markup

if __name__ == '__main__':
    bot.infinity_polling()