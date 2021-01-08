#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

import handlers as handlers

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    
    token = os.environ.get("POKER_BOT_TOKEN")

    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(ConversationHandler(
                                        entry_points=[CommandHandler('start', handlers.start)],
                                        states={
                                                handlers.START: [CallbackQueryHandler(handlers.start)],

                                                handlers.PREFLOP: [MessageHandler(Filters.text & ~Filters.command, handlers.preFlopHandler),
                                                                   CallbackQueryHandler(handlers.helpHandler)],

                                                handlers.FLOP: [MessageHandler(Filters.text & ~Filters.command, handlers.flopHandler)],

                                                handlers.TURN: [MessageHandler(Filters.text & ~Filters.command, handlers.turnHandler)],
                                                },
                                        fallbacks=[CommandHandler('start', handlers.start)]
                                        )
                    )

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()