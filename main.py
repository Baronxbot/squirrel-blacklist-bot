#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2020, SquirrelNetwork"
__credits__ = ["https://github.com/BluLupo"]
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__repository__ = "https://github.com/Squirrel-Network/Resources/blob/master/base_telegram_bot_Python"
__status__ = "Development"

### IMPORT ###
import logging
import datetime
from config import Config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# Function for button
def build_menu(buttons, n_cols, header_buttons=False, footer_buttons=False):
  menu=[buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

# Start function
def start(update, context):
    buttons = []
    user = "@"+update.message.from_user.username
    date = datetime.datetime.utcnow().isoformat()
    buttons.append(InlineKeyboardButton('Bottone', callback_data='callbacktest'))
    buttons.append(InlineKeyboardButton('Info', callback_data='info'))
    menu = build_menu(buttons,2)
    update.message.reply_text("👋 Ciao {} e benvenuto nel mio bot \n\n Sono le {} \n\n 🤖 Versione: {}".format(user,date, __version__), reply_markup=InlineKeyboardMarkup(menu))
    
# Edit start menu function
def update_Start(update, context):
    bot = context.bot
    query = update.callback_query
    q = query.data
    print(query)
    buttons = []
    menu = build_menu(buttons,2)
    if q == 'info':
      # print("A")
      buttons.append(InlineKeyboardButton('Indietro', callback_data='back'))
      menu = build_menu(buttons,2)
      query.edit_message_text("Sei nella sezione info \n bot sviluppando usando la base di squirrel network", reply_markup=InlineKeyboardMarkup(menu))
    elif q == 'callbacktest':
      # print("B")
      buttons.append(InlineKeyboardButton('Indietro', callback_data='back'))
      menu = build_menu(buttons,2)
      query.edit_message_text("polettone", reply_markup=InlineKeyboardMarkup(menu))      


    
def main():
    updater = Updater(Config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    #Start handler
    start_handler = CommandHandler('start', start)
    edit_start = CallbackQueryHandler(update_Start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(edit_start)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
