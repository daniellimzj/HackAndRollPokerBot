from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

helpMenu = build_menu([InlineKeyboardButton(text = "Help 🆘", callback_data = "help")], n_cols = 1, header_buttons= None, footer_buttons=None)
startMenu = build_menu([InlineKeyboardButton(text = "Back to Start ↩️", callback_data = "start")], n_cols = 1, header_buttons= None, footer_buttons=None)
