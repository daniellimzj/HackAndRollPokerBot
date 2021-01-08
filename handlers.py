import datetime
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

import menus as menus
import cardParser as cardParser


START, PREFLOP, FLOP, TURN, END = range(5)



def start(update, context):

    global user
    global chatid

    # Some initialisation
    if (update.message):
        user = update.message.from_user
        chatid = update.message.chat.id

    #Actual message
    context.bot.send_message(text = f'Start! Please enter the cards in your hand, or use the help button!',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.helpMenu))
    return PREFLOP

def preFlopHandler(update, context):

    message = update.message.text

    cards = cardParser.parseCardsInHand(message)

    if (cards == "error"):
        context.bot.send_message(text = f'Error! Try again!',
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return PREFLOP
    
    context.bot.send_message(text = f'Your cards are <b>{cards[0]}</b> and <b>{cards[1]}</b>',
                            chat_id = chatid
                            ,
                            parse_mode = ParseMode.HTML,
                            reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return FLOP

def flopHandler(update, context):

    query = update.callback_query
    context.bot.send_message(text = f'FLOP',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return TURN

def turnHandler(update, context):

    query = update.callback_query
    context.bot.send_message(text = f'TURN',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return START

def helpHandler(update, context):

    context.bot.send_message(text = f'HELP',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return START
    