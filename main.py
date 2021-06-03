#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2020, SquirrelNetwork"
__credits__ = ["https://github.com/SalvatoreCalo"]
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__repository__ = "https://github.com/Squirrel-Network/Resources/blob/master/base_telegram_bot_Python"
__status__ = "Development"

### IMPORT ###
import logging
import requests
from config import Config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def build_menu(buttons, n_cols, header_buttons=False, footer_buttons=False):
  menu=[buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

# Start function
def start(update, context):
    user = "@"+ update.message.from_user.username
    buttons = []
    buttons.append(InlineKeyboardButton('HOW IT WORKS?', callback_data='info'))
    menu = build_menu(buttons,2)
    update.message.reply_text("👋 Ciao {}, tramite questo  bot puoi scoprire se un utente è in blacklist o meno \n\n Made with ❤️ by @SquirrelNetwork \n\n 🤖 Versione: {}".format(user, __version__), reply_markup=InlineKeyboardMarkup(menu))

# Update start
def update_start(update, context):
    query = update.callback_query
    q = query.data
    print(query)
    buttons = []
    menu = build_menu(buttons,2)
    if q == 'info':
      print("A")
      buttons.append(InlineKeyboardButton('Indietro', callback_data='back'))
      menu = build_menu(buttons,2)
      query.edit_message_text("COmandi del bot: \n\n /checkme: controlla se sei in blacklist o no \n\n /check id: check if a user is in our blacklist", reply_markup=InlineKeyboardMarkup(menu))
    elif q == 'back':
      print("B")
      buttons.append(InlineKeyboardButton('HOW IT WORKS?', callback_data='info'))
      menu = build_menu(buttons,2)
      query.edit_message_text("👋 Bentornato, tramite questo  bot puoi scoprire se un utente è in blacklist o meno \n\n Made with ❤️ by @SquirrelNetwork \n\n 🤖 Versione: {}".format(__version__), reply_markup=InlineKeyboardMarkup(menu))

# Check Me function
def checkme(update, context):
    user = update.effective_message.from_user
    index = user.id
    payload = {'key1': 'value1', 'key2': 'value2'}
    api = requests.get('https://api.nebula.squirrel-network.online/v1/blacklist/{}'.format(index), params=payload)
    if payload['key1'] != '{"error":"The user was not superbanned or you entered an incorrect id"}':
      update.message.reply_text("Ben fatto! Attualmente non sei nella nostra blacklist! :)")
    else: 
      update.message.reply_text("You are in our blacklist!. :(")

# Check by id function
def check(update, context):
    user = update.effective_message.from_user
    index = context.args[0]
    payload = {'key1': 'value1', 'key2': 'value2'}
    api = requests.get('https://api.nebula.squirrel-network.online/v1/blacklist/{}'.format(index), params=payload)
    try:
      if payload['key1'] != '{"error":"The user was not superbanned or you entered an incorrect id"}':
        update.message.reply_text("Questo id non sembra essere presente nella nostra blacklist")
      else: 
        update.message.reply_text("Questo utente è nella nostra blacklist. :(")
    except (IndexError, ValueError):
        update.message.reply_text('si prega di inserire un id')

def main():
    updater = Updater(Config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    #Start handler
    start_handler = CommandHandler('start', start)
    edit_start = CallbackQueryHandler(update_start)
    checkme_handler = CommandHandler('checkme', checkme)
    check_handler = CommandHandler('check', check)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(edit_start)
    dispatcher.add_handler(checkme_handler)
    dispatcher.add_handler(check_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

