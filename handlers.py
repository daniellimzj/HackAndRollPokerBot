import datetime
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

import menus as menus

START, PREFLOP, FLOP, TURN = range(4)

def start(update, context):

    # Some initialisation
    global user
    global chatid
    user = update.message.from_user
    chatid = update.message.chat.id

    #Actual message
    context.bot.send_message(text = f'Start! Please enter the cards in your hand.',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.menu))
    return PREFLOP

def preFlopHandler(update, context):

    query = update.callback_query
    context.bot.send_message(text = f'PREFLOP',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.menu))
    return FLOP

def flopHandler(update, context):

    query = update.callback_query
    context.bot.send_message(text = f'FLOP',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.menu))
    return TURN

def turnHandler(update, context):

    query = update.callback_query
    context.bot.send_message(text = f'TURN',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.menu))
    return START