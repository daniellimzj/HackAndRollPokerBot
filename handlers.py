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
    chatid = update.message.chat.id

    cards = cardParser.parseCardsInHand(message)

    if (cards == "error"):
        context.bot.send_message(text = f'Error with parsing your input! PLease try again:',
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return PREFLOP

    if (not isHandValid(cards)):
        context.bot.send_message(text = f"I've detected a duplicate card! Please try again:",
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return PREFLOP
    
    knownCards.extend(cards)

    oddsOfPair = oddsCalc.findPairOdds(knownCards, "preflop")
    oddsOfTrips = oddsCalc.findTripsOdds(knownCards, "preflop")
    oddsOfFlush = oddsCalc.findFlushOdds(knownCards, "preflop")
    oddsOfQuads = oddsCalc.findQuadsOdds(knownCards, "preflop")

    text = f'The cards in your hand are <b>{cards[0]}</b> and <b>{cards[1]}</b>' + ".\n\n"

    text += "<b>Probabilities:</b>\n"

    if (oddsOfPair and oddsOfTrips != 100 and oddsOfFlush != 100 and oddsOfQuads != 100):
        text += "Pair: " + str(oddsOfPair) + "%\n"

    if (oddsOfTrips and oddsOfFlush != 100 and oddsOfQuads != 100):
        text += "Three of a Kind: " + str(oddsOfTrips) + "%\n"
    
    if (oddsOfFlush and oddsOfQuads != 100):
        text += "Flush: " + str(oddsOfFlush) + "%\n"
    
    if (oddsOfQuads):
        text += "Quads: " + str(oddsOfQuads) + "%\n"
    
    text += "\nNow enter the cards in the flop, or press the back to start button to start a new round:"

    context.bot.send_message(text = text,
                            chat_id = chatid,
                            parse_mode = ParseMode.HTML,
                            reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return FLOP

def flopHandler(update, context):

    message = update.message.text
    chatid = chatid = update.message.chat.id

    cards = cardParser.parseCardsInFlop(message)

    if (cards == "error"):
        context.bot.send_message(text = f'Error with parsing your input! PLease try again:',
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return FLOP

    if (not isFlopValid(cards)):
        context.bot.send_message(text = f"I've detected a duplicate card! Please try again:",
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return FLOP

    knownCards.extend(cards)

    oddsOfPair = oddsCalc.findPairOdds(knownCards, "postflop")
    oddsOfTrips = oddsCalc.findTripsOdds(knownCards, "postflop")
    oddsOfFlush = oddsCalc.findFlushOdds(knownCards, "postflop")
    oddsOfQuads = oddsCalc.findQuadsOdds(knownCards, "postflop")

    text = f'The cards in the flop are <b>{cards[0]}</b>, <b>{cards[1]}</b> and <b>{cards[2]}</b>.' + "\n\n"

    text += "<b>Probabilities:</b>\n"

    if (oddsOfPair and oddsOfTrips != 100 and oddsOfFlush != 100 and oddsOfQuads != 100):
        text += "Pair: " + str(oddsOfPair) + "%\n"

    if (oddsOfTrips and oddsOfFlush != 100 and oddsOfQuads != 100):
        text += "Three of a Kind: " + str(oddsOfTrips) + "%\n"
    
    if (oddsOfFlush and oddsOfQuads != 100):
        text += "Flush: " + str(oddsOfFlush) + "%\n"
    
    if (oddsOfQuads):
        text += "Quads: " + str(oddsOfQuads) + "%\n"
    
    text += "\nNow enter the turn card, or press the back to start button to start a new round:"

    context.bot.send_message(text = text,
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return TURN

def turnHandler(update, context):

    message = update.message.text
    chatid = update.message.chat.id

    card = cardParser.parseCardsInTurn(message)

    if (card == "error"):
        context.bot.send_message(text = f'Error with parsing your input! PLease try again:',
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return TURN

    if (not isTurnValid(card)):
        context.bot.send_message(text = f"I've detected a duplicate card! Please try again:",
                                chat_id = chatid,
                                parse_mode = ParseMode.HTML,
                                reply_markup = InlineKeyboardMarkup(menus.startMenu))
        return TURN
    
    knownCards.append(card)

    oddsOfPair = oddsCalc.findPairOdds(knownCards, "turn")
    oddsOfTrips = oddsCalc.findTripsOdds(knownCards, "turn")
    oddsOfFlush = oddsCalc.findFlushOdds(knownCards, "turn")
    oddsOfQuads = oddsCalc.findQuadsOdds(knownCards, "turn")

    text = f"The turn card is <b>{card}</b>." + "\n\n"

    text += "<b>Probabilities:</b>\n"

    if (oddsOfPair and oddsOfTrips != 100 and oddsOfFlush != 100 and oddsOfQuads != 100):
        text += "Pair: " + str(oddsOfPair) + "%\n"

    if (oddsOfTrips and oddsOfFlush != 100 and oddsOfQuads != 100):
        text += "Three of a Kind: " + str(oddsOfTrips) + "%\n"
    
    if (oddsOfFlush and oddsOfQuads != 100):
        text += "Flush: " + str(oddsOfFlush) + "%\n"

    if (oddsOfQuads):
        text += "Quads: " + str(oddsOfQuads) + "%\n"
    
    text += "\nPress the back to start button to start a new round:"

    context.bot.send_message(text = text,
                             chat_id = chatid,
                             parse_mode = ParseMode.HTML,
                             reply_markup = InlineKeyboardMarkup(menus.startMenu))
    return START

def helpHandler(update, context):

    query = update.callback_query

    text = "Help Menu: \n\n"
    text += "- Use C, D, H and S to represent the suits of your cards.\n"
    text += "- Use 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A to represent the numbers of your cards. Take note that 10 is represented by T.\n"
    text += "- The format of each card is number then suit: e.g. KH, TC or 4D.\n"
    text += "- When entering the cards in your hand or in the flop, enter each card separated by a space. e.g. KH KD for your hand, or 5D 6C 7S for the flop.\n"
    text += "- If you've already made a better hand, the probabilities of obtaining worse hands will not be shown."
    text += "- Currently, this bot only calculates the probabilities of making a pair, three of a kind, flush, and quads. If the probability is 0, it won't be shown.\n\n"
    text += "If you have questions, please Telegram @goopod or @ivannedly. Thank you for using this service! Hope you win!"

    if (query.data == "help"):
        context.bot.send_message(text = text,
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
    