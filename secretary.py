#!/usr/bin/python
import sys
import time
import telepot
import storage

def handle(msg):
    global storage
    content_type, chat_type, chat_id = telepot.glance(msg)
    print content_type, chat_type, chat_id

    if content_type != 'text': return
    storage.store_message(msg)

TOKEN = sys.argv[1]  # get token from command-line

storage = storage.Storage("messages.sqlite")

bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handle)

print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)

storage.finalize() # FIXME: unreacheable
