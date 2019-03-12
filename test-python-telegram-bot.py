'''

@author: smile
'''

from telegram.ext import Updater
from telegram.ext import CommandHandler

from telegram.ext import MessageHandler, Filters
from telegram import MessageEntity

import pdfkit
from tempfile import *

BOT_TOKEN='===PASTE-API-TOKEN-HERE==='

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="echo: "+update.message.text)


def url(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="i've got your link, processing it...")
    url = update.message.text
    
    f = NamedTemporaryFile(delete=True)
    
    pdf = pdfkit.from_url(url, False)
    
    f.write(pdf)
    
    f.seek(0)
    
    
    bot.send_message(chat_id=update.message.chat_id, text="done "+f.name)
    bot.send_document(chat_id=update.message.chat_id, document = f, filename="result.pdf")
    
    f.close()

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':

    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    
    dispatcher.add_handler(start_handler)
  
    
    
    url_handler = MessageHandler( Filters.text & (Filters.entity(MessageEntity.URL) |
                    Filters.entity(MessageEntity.TEXT_LINK)), url)
    dispatcher.add_handler(url_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    
    updater.start_polling()
    updater.idle()
    updater.stop()
