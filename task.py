
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from credits import bot_token

import requests
from bs4 import BeautifulSoup as bs

bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(update.effective_chat.id, "Давай начнем переписку")

def anekdot(update, context):
    context.bot.send_message(update.effective_chat.id, "Чтобы получить анекдот набери любую цифру: ")


def unknow(update, context):
    context.bot.send_message(update.effective_chat.id, "Неизвестная для меня команда")

def message(update, context):
    if update.message.text == "Привет":
        context.bot.send_message(update.effective_chat.id, "Привет, Антон. Я твой первый телеграм-бот")
    elif update.message.text == "привет":
        context.bot.send_message(update.effective_chat.id, "Привет, Антон. Я твой первый телеграм-бот")
    else:
        context.bot.send_message(update.effective_chat.id, "Пароль?")

def jokes(update, context):
    url = 'https://www.anekdot.ru'
    response = requests.get(url).text
    soup = bs(response, 'html.parser')
    fun = soup.find_all('div', class_='text')
    list_of_jokes = [c.text for c in fun]
    if update.message.text.lower() in '123456789':
        context.send_message(update.effective_chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        context.send_message(update.effective_chat.id, 'Набери любую цифру от 1 до 9')

def get_day(update, context):
    keyboard = [
        [InlineKeyboardButton("Понедельник", callback_data='1'),
         InlineKeyboardButton("Вторник", callback_data='2'),
         InlineKeyboardButton("Среда", callback_data='3'),
         InlineKeyboardButton("Четверг", callback_data='4'),
         InlineKeyboardButton("Пятница", callback_data='5')]
    ]
    update.message.reply_text("Выбери день недели", reply_markup=InlineKeyboardMarkup(keyboard))

def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        context.bot.send_message(update.effective_chat.id, "Понедельник")
    elif query.data == '2':
        context.bot.send_message(update.effective_chat.id, "Вторник")
    elif query.data == '3':
        context.bot.send_message(update.effective_chat.id, "Среда")
    elif query.data == '4':
        context.bot.send_message(update.effective_chat.id, "Четверг")
    elif query.data == '5':
        context.bot.send_message(update.effective_chat.id, "Пятница")

button_handler = CallbackQueryHandler(button)
start_handler = CommandHandler('start', start)
anekdot_handler = CommandHandler('anekdot', anekdot)
getday_handler = CommandHandler('getday', get_day)
unknow_handler = MessageHandler(Filters.command, unknow)
message__handler = MessageHandler(Filters.text, message)
jokes__handler = MessageHandler(Filters.text, jokes)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(anekdot_handler)
dispatcher.add_handler(getday_handler)
dispatcher.add_handler(unknow_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(message__handler)
dispatcher.add_handler(jokes__handler)

updater.start_polling()
updater.idle()

