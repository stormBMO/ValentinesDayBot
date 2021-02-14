# coding=utf-8
import shutil
from time import sleep
from random import randint
import os
import telebot
import threading

# ----------------------------------------------------------------------------
token_bot = '1654475418:AAHZ8MOBnHgH2t66qL4jvSbsrUqrFymufF8'
bot = telebot.TeleBot(token_bot)
flag_for_schedule = 0
keyboard_hider = telebot.types.ReplyKeyboardRemove()
channel_id = "@pt_demid"

users = {

}

#------------------------------Tread start----------------------------------

#------------------------------States----------------------------------------
user_states = {}

S_NOSUB = "0"  # Начало нового диалога
S_START = "1"
S_ENTER_NAME = "2"
S_SEND_PIC = "3"

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
    chat_id = message.from_user.id
    if chat_id not in user_states:
        user_states[chat_id] = S_NOSUB
    if not is_subscribed(channel_id, message.from_user.id):
        user_states[chat_id] = S_NOSUB
        bot.send_message(message.chat.id, "Для использования бота подпишись на @pt_demid, а затем опять напиши /start")
    else:
        user_states[chat_id] = S_START
        main_func(message)


#------------------------------Main logic--------------------------------------

def main_func(message):
    chat_id = message.chat.id
    if message.text == "/start":
        markup = generate_start_markup()
        bot.send_message(message.chat.id,
                         "Привет!\nЭто чат-бот PrimeTime для валентинок. Порадуй весточкой вторую половинку, друзей или своего краша. Жди валентинки вечером 14 февраля.\n\nЧтобы отправить валентинку, нажми кнопку ниже 🔽",
                         reply_markup=markup)
    elif message.text == "Отправить валентинку":
        user_states[chat_id] = S_ENTER_NAME
        bot.send_message(message.chat.id,
                         "Сначала напиши, кому ты хочешь отправить валентинку. Для этого укажи ник в инстаграмме/id во ВКонтакте.",
                         reply_markup=keyboard_hider)
        bot.register_next_step_handler(message, get_valentine)


def get_valentine(message):
    if user_states[message.chat.id] == S_ENTER_NAME:
        users[message.from_user.id] = message.text
        bot.send_message(message.chat.id, "Теперь отправь валентинку")
        user_states[message.chat.id] = S_SEND_PIC


# -----------------------------Photo--------------------------------------------
@bot.message_handler(content_types=["photo"])
def get_photo_messages(message):
    if user_states[message.chat.id] == S_SEND_PIC:
        to_who = users[message.from_user.id]
        to_who = to_who + "0"
        markup = generate_start_markup()
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        photo_name = to_who + ".jpg"
        backup_name = to_who[:-1]
        photo_name = photo_name.translate({ord(c): None for c in '?!/;:\\'})
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
        users[message.from_user.id] = ""
        user_states[message.chat.id] = S_START
    else:
        bot.send_message(message.chat.id, "Для начала пройди все пункты до этого!")

# -----------------------------keyboards----------------------------------------

def generate_start_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Отправить валентинку')
    markup.row(button1)
    return markup

#-----------------------------Other Listeners----------------------------------
@bot.message_handler(content_types=['sticker'])
def sticker_stop(message):
    print(message)
    bot.send_sticker(message.from_user.id, 'CAACAgQAAxkBAAIH1V79skuRxW2HHxSIguJ1xG3zN3T3AAJXBwACzfXABHlZqZRf_0W6GgQ')
    bot.send_message(message.from_user.id, "Я не понимаю стикеров, пиши /start")


@bot.message_handler(content_types=['voice'])
def voice_stop(message):
    bot.send_message(message.from_user.id, "Я не понимаю речь, пиши /start")

if __name__ == '__main__':
    bot.infinity_polling()
