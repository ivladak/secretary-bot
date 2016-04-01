#!/usr/bin/python
import os
import sys
import time
import telepot
import storage
from secretary_exceptions import *
from classifier import MessageClassifier
from representations import write_html
from datetime import datetime

DIGEST_DIR = "digest"

def handle(msg):
    global storage
    global bot
    content_type, chat_type, chat_id = telepot.glance(msg)
    print content_type, chat_type, chat_id

    if content_type != 'text': return
    if msg['text'].strip().lower() == '/digest':
        classes = storage.digest(chat_id, MessageClassifier())
        filename = DIGEST_DIR + "/" + "-".join(str(datetime.utcnow()).split()) + ".html"
        write_html(classes, filename)
        bot.sendChatAction(chat_id, 'upload_document')
        bot.sendDocument(chat_id, open(filename, 'rb'))
    else:
        storage.store_message(msg)

TOKEN = sys.argv[1]  # get token from command-line

storage = storage.Storage("messages.sqlite")
if not os.path.exists(DIGEST_DIR):
    os.mkdir(DIGEST_DIR)
else:
    if not os.path.isdir(DIGEST_DIR):
        raise DigestDirNotWritable(DIGEST_DIR)

bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handle)

print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)

storage.finalize() # FIXME: unreacheable
