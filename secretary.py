#!/usr/bin/python
import sys
import time
import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print content_type, chat_type, chat_id
    # Do your stuff according to `content_type` ...
    if content_type != 'text':
        return
    if 'hello' in msg['text']:
        bot.sendMessage(chat_id, "Hello, master!") 
    else:
        bot.sendMessage(chat_id, "Say what? " + str(msg['date'])) 

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handle)
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)
