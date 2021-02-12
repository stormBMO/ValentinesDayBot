# coding=utf-8
import telebot

# ----------------------------------------------------------------------------
token_bot = '1654475418:AAHZ8MOBnHgH2t66qL4jvSbsrUqrFymufF8'
bot = telebot.TeleBot(token_bot)
flag_for_schedule = 0
keyboard_hider = telebot.types.ReplyKeyboardRemove()
to_who = ""

# ----------------------------------------------------------------------------


# -----------------------------Text-------------------------------------------
@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "/start":
        markup = generate_start_markup()
        bot.send_message(message.chat.id,
                         "Привет! Это бот для валентинок (не знаю, придумайте сюда текст - я вставлю). Чтобы отправить валентинку, нажми кнопку ниже",
                         reply_markup=markup)

    elif message.text == "Отправить валентинку":
        bot.send_message(message.chat.id, "Сначала отпаравь мне кому ты хочешь отправить валентинку (Можешь инстаграмм, например), затем отправь саму валентинку",
                         reply_markup=keyboard_hider)
        bot.register_next_step_handler(message, get_valentine)


#------------------------------Main logic--------------------------------------

def get_valentine(message):
    global to_who
    to_who = message.text
    bot.send_message(message.chat.id, "Теперь отправивь валентинку")



# -----------------------------Photo--------------------------------------------
@bot.message_handler(content_types=["photo"])
def get_photo_messages(message):
    global to_who
    if to_who == "":
        bot.send_message(message.chat.id, "Для начала пройди все пункты до этого!")
    else:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        print('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(to_who + ".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(message.chat.id, "Супер, " + to_who + " получит твою валентинку.")
        to_who = ""

# -----------------------------keyboards----------------------------------------

def generate_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Отправить валентинку')
    markup.row(button1)
    return markup


if __name__ == '__main__':
    bot.infinity_polling()
