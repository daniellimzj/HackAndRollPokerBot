"""
HydRC4nics bot

Allows users to send commands (if they are administrators) and view data from RC4's smart hydroponics garden
"""

import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

from . import handlers as hl

from .. import config
from .. import db

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# TOKEN to communicate with the correct bot
TOKEN = "1578758398:AAGnbbNlC8K1AAsLo69-0dcGypgVrYSiWww"


"""
Various functions
"""

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def main():

    """Start the bot."""
    # Create the Updater and pass it your bogit oullt's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(ConversationHandler(
                                        entry_points=[CommandHandler('start', hl.start)],
                                        states={
                                                hl.INITIAL: [CallbackQueryHandler(hl.startOver)],

                                                hl.START: [CallbackQueryHandler(hl.startHandler)],

                                                hl.ACTUATORS: [CallbackQueryHandler(hl.startOver, pattern='^START$'),
                                                               CallbackQueryHandler(hl.ActuatorsHandler)],

                                                hl.COMMAND: [CallbackQueryHandler(hl.startOver, pattern='^START$'),
                                                             MessageHandler(Filters.text & (~Filters.command), hl.commandHandler)],

                                                hl.DATA: [CallbackQueryHandler(hl.startOver, pattern = '^START$'),
                                                          CallbackQueryHandler(hl.dataHandler)],

                                                hl.SENSORS: [CallbackQueryHandler(hl.startOver, pattern='^START$'),
                                                             CallbackQueryHandler(hl.sensorsHandler)],
                                                
                                                hl.READINGS: [CallbackQueryHandler(hl.startOver, pattern='^START$'),
                                                              MessageHandler(Filters.text & (~Filters.command), hl.readingsHandler)],
                                                },
                                        fallbacks=[CommandHandler('start', hl.start)]
                                        )
                    )


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()