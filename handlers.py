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
    global knownCards

    knownCards = []
    print(knownCards)

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

    if (not isHandValid(cards)):
        context.bot.send_message(text = f"I've detected a duplicate card!",
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return PREFLOP
    
    knownCards.extend(cards)
    print(knownCards)

    context.bot.send_message(text = f'Your cards are <b>{cards[0]}</b> and <b>{cards[1]}</b>',
                            chat_id = chatid,
                            parse_mode = ParseMode.HTML,
                            reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return FLOP

def flopHandler(update, context):

    message = update.message.text

    cards = cardParser.parseCardsInFlop(message)

    if (cards == "error"):
        context.bot.send_message(text = f'Error! Try again!',
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return FLOP

    if (not isFlopValid(cards)):
        context.bot.send_message(text = f"I've detected a duplicate card!",
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return FLOP

    knownCards.extend(cards)

    context.bot.send_message(text = f'Your cards are <b>{cards[0]}</b>, <b>{cards[1]}</b> and <b>{cards[2]}</b>',
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return TURN

def turnHandler(update, context):

    message = update.message.text

    card = cardParser.parseCardsInTurn(message)

    if (card == "error"):
        context.bot.send_message(text = f'Error! Try again!',
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return TURN

    if (not isTurnValid(card)):
        context.bot.send_message(text = f"I've detected a duplicate card!",
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return TURN

    context.bot.send_message(text = f'Your card is <b>{card}</b>,',
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

def startOverHandler(update, context):

    

def isHandValid(cards):
    return (cards[0] != cards[1] and cards[0] not in knownCards and cards[1] not in knownCards) 

def isFlopValid(cards):
    return (cards[0] != cards[1] and cards[1] != cards[2] and cards[0] != cards[2] and cards[0] not in knownCards and cards[1] not in knownCards and cards[2] not in knownCards)

def isTurnValid(card):
    return (card not in knownCards)
    