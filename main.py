import os
import requests
import random
import logging
import yfinance as yf
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = 'TOKEN'
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def prices(update, context):
    itembtna = telegram.KeyboardButton('BTC-USD')
    itembtnb = telegram.KeyboardButton("ETH-USD")
    itembtnc = telegram.KeyboardButton("USDT-USD")
    itembtnd = telegram.KeyboardButton("BNB-USD")
    itembtne = telegram.KeyboardButton("USDC-USD")
    itembtnh = telegram.KeyboardButton("SOL-USD")
    itembtni = telegram.KeyboardButton("XRP-USD")
    itembtnj = telegram.KeyboardButton("LUNA1-USD")
    markup = telegram.ReplyKeyboardMarkup(
        [[itembtna, itembtnb], [itembtnc, itembtnd, itembtne], [itembtnh, itembtni, itembtnj]], one_time_keyboard=True)

    # markup.row(itembtna, itembtnb)
    # markup.row(itembtnc, itembtnd, itembtne)
    # markup.row(itembtnh,itembtni, itembtnj)
    update.message.reply_text("Choose the cryptocurrency:", reply_markup=markup)





def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! How can i help you. check /help for more informations to know how to use the bot')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! \n'
                              'This bot is made for people who want see the price of the cryptocurrency \n'
                              'Click in /prices then you will see all the cryptocurrencies, choose one and wait until you get the price of that cryptocurrency.')


def echo(update, context):

    """Echo the user message."""
    update.message.reply_text('We are laoding the price, wait few seconds...')
    t = update.message.text
    m = yf.Ticker(t)
    hist = m.history(period='max')
    data = str(hist['Close'][-1])
    user = update.message.from_user
    name = m.info['name']
                                                        #data = round(data,2)
    update.message.reply_text('HI '+user.first_name+' The price of '+ name +' is :'+str(round(float(data),2)) +'$')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("prices", prices))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
