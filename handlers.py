import datetime
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

import menus as menus
import cardParser as cardParser
import oddsCalculator as oddsCalc


START, PREFLOP, FLOP, TURN, END = range(5)



def start(update, context):

    global user
    global chatid
    global knownCards

    knownCards = []

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

    oddsOfPair = oddsCalc.findPairOdds(knownCards, "preflop")
    oddsOfTrips = oddsCalc.findTripsOdds(knownCards, "preflop")
    oddsOfFlush = oddsCalc.findFlushOdds(knownCards, "preflop")

    text = f'The cards in your hand are <b>{cards[0]}</b> and <b>{cards[1]}</b>' + ".\n\n"

    text += "<b>Probabilities:</b>\n"

    if (oddsOfPair):
        text += "Pair: " + str(oddsOfPair) + "%\n"

    if (oddsOfTrips):
        text += "Three of a Kind: " + str(oddsOfTrips) + "%\n"
    
    if (oddsOfFlush):
        text += "Flush: " + str(oddsOfFlush) + "%\n"
    
    text += "\nNow enter the cards in the flop, or press the back to start button to start a new round:"

    context.bot.send_message(text = text,
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

    oddsOfPair = oddsCalc.findPairOdds(knownCards, "postflop")
    oddsOfTrips = oddsCalc.findTripsOdds(knownCards, "postflop")
    oddsOfFlush = oddsCalc.findFlushOdds(knownCards, "postflop")

    text = f'The cards in the flop are <b>{cards[0]}</b>, <b>{cards[1]}</b> and <b>{cards[2]}</b>.' + "\n\n"

    text += "<b>Probabilities:</b>\n"

    if (oddsOfPair):
        text += "Pair: " + str(oddsOfPair) + "%\n"

    if (oddsOfTrips):
        text += "Three of a Kind: " + str(oddsOfTrips) + "%\n"
    
    if (oddsOfFlush):
        text += "Flush: " + str(oddsOfFlush) + "%\n"
    
    text += "\nNow enter the turn card, or press the back to start button to start a new round:"

    context.bot.send_message(text = text,
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
    
    knownCards.append(card)

    oddsOfPair = oddsCalc.findPairOdds(knownCards, "turn")
    oddsOfTrips = oddsCalc.findTripsOdds(knownCards, "turn")
    oddsOfFlush = oddsCalc.findFlushOdds(knownCards, "turn")

    text = f"The turn card is <b>{card}</b>." + "\n\n"

    text += "<b>Probabilities:</b>\n"

    if (oddsOfPair):
        text += "Pair: " + str(oddsOfPair) + "%\n"

    if (oddsOfTrips):
        text += "Three of a Kind: " + str(oddsOfTrips) + "%\n"
    
    if (oddsOfFlush):
        text += "Flush: " + str(oddsOfFlush) + "%\n"
    
    text += "\nPress the back to start button to start a new round:"

    context.bot.send_message(text = text,
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return START

def helpHandler(update, context):

    query = update.callback_query

    if (query.data == "help"):
        context.bot.send_message(text = f'HELP',
                                 chat_id = chatid,
                                 parse_mode = ParseMode.HTML,
                                 reply_markup = InlineKeyboardMarkup(menus.startMenu))

    return START



def isHandValid(cards):
    return (cards[0] != cards[1] and cards[0] not in knownCards and cards[1] not in knownCards) 

def isFlopValid(cards):
    return (cards[0] != cards[1] and cards[1] != cards[2] and cards[0] != cards[2] and cards[0] not in knownCards and cards[1] not in knownCards and cards[2] not in knownCards)

def isTurnValid(card):
    return (card not in knownCards)
    