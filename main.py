# coding=utf-8
import shutil
import os
import telebot
from telebot.apihelper import ApiException
# ----------------------------------------------------------------------------
token_bot = '1654475418:AAHZ8MOBnHgH2t66qL4jvSbsrUqrFymufF8'
bot = telebot.TeleBot(token_bot)
flag_for_schedule = 0
keyboard_hider = telebot.types.ReplyKeyboardRemove()
to_who = ""
channel_id = "@pt_demid"
# -----------------------------Text-------------------------------------------

def is_subscribed(channel_id, user_id):
    status = ['creator', 'administrator', 'member']
    user_status = str(bot.get_chat_member(channel_id, user_id).status)
    if user_status in status:
        return True
    else:
        return False

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if not is_subscribed(channel_id, message.from_user.id):
        bot.send_message(message.chat.id, "Для использования бота подпишись на @pt_demid, а затем опять напиши /start")
    else:
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
        to_who = to_who + "0"
        markup = generate_start_markup()
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        photo_name = to_who + ".jpg"
        backup_name = to_who[:-1]
        backup_path_name = photo_name
        with open(photo_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        i = 1
        while True:
            if os.path.exists("photo/" + photo_name):
                to_who = to_who[:-1]
                to_who = to_who + str(i)
                i = i + 1
                photo_name = to_who + ".jpg"
            else:
                os.rename(backup_path_name, photo_name)
                shutil.move(photo_name, "photo")
                break
        bot.send_message(message.chat.id, "Супер, " + backup_name + " получит твою валентинку.", reply_markup=markup)
        to_who = ""

# -----------------------------keyboards----------------------------------------

def generate_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Отправить валентинку')
    markup.row(button1)
    return markup


if __name__ == '__main__':
    bot.infinity_polling()
