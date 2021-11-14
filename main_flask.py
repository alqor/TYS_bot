'''
Simple telegram bot to seat N people to N seats
For local launch activate first
venv_path => D:\PY\py_venv\telebot_flask_venv\Scripts\Activate.ps1

environment variables must be set:
API_TOKEN - both local and prod
HEROKU - just in prod (to define where we launch the bot)
'''

import logging
import random
import os

from flask import Flask, request

import telebot

from parameters import *

print(API_TOKEN)
# initialliza the bot
bot = telebot.TeleBot(API_TOKEN)

# to get info in console
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# hanlde bot commands and text listener

class SeatPersones:
    def __init__(self):
        self.persons = []
        self.seats = []

    def take_your_seat(self):
        random.shuffle(self.seats)
        return zip(self.persons, self.seats)

tys = SeatPersones()

@bot.message_handler(commands=['help'])
def handler_start(message):
    reply = "Hello, I will help you to assign the seats numbers for the same quantity of persons.\n\
For example, if the persons are: \n\
\t\t\tCthulhu, Sauron, Dart Vader \n\
and seats are: \n\
\t\t\t23, 56, 32\n\
The result could be:\n\
Cthulhu - 56\n\
Sauron - 23\n\
Dart Vader - 32\n\
    \n\
Type /start when you're ready to provide the info."

    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['start'])
def handler_start(message):
    '''
    Will ask to provide list of names and list of seats,
    then reply with random seats assigned for each person
    '''
    persons_ask = 'Please provide list of persons separated by comma.'
    msg = bot.send_message(message.chat.id, persons_ask)
    bot.register_next_step_handler(msg, process_seats)


def process_seats(message):
    chat_id = message.chat.id

    persons_list = message.text.split(',')
    tys.persons = [i.strip() for i in persons_list] 
    # print(tys.persons)

    seats_len = len(tys.persons)
    seats_ask = f'Please provide list of seats numbers separated by comma. Total: {seats_len}.'
    msg = bot.reply_to(message, seats_ask)
    bot.register_next_step_handler(msg, process_answer)


def process_answer(message):
    chat_id = message.chat.id

    seats_list = message.text.split(',')
    tys.seats = seats_list 

    if len(tys.persons) == len(seats_list):
        reply_dict = dict(tys.take_your_seat())
        reply = 'Here are your seats:\n'
        for person, seat in reply_dict.items():
            reply+= f'{person} - {seat}\n'
        
        bot.send_message(message.chat.id, reply)

    else:
        wrong_length = "Sorry, seems that the numbers of persons and seats are not equal. Type /start to try again. "
        bot.send_message(message.chat.id, wrong_length)


def main(bot):
    '''
    The function checks if bot runs local or on heroku
    so we need to add HEROKU var to PATH variables on heroku app.
    If we are on heroku app, run simple flask server.

    Or if we're on local machine just start polling the bot.
    In this case remove webhook, because it will throw an error if the one left from previous launch.
    '''

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    if "HEROKU" in list(os.environ.keys()):
        server = Flask(__name__)

        @server.route("/", methods=['POST'])
        def getMessage():
            bot.process_new_updates(
                [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "I'm looking for answer.", 200

        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(url=WEBHOOK_HOST)
            return "I'm alive and waiting for your messages", 200

        server.run(host=WEBHOOK_LISTEN, port=WEBHOOK_PORT)

    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)


if __name__ == '__main__':
    main(bot)
