#!/usr/bin/env python
import os
import sys
import time
import telepot
import storage
from Queue import Queue
from urlparse import urlparse
from datetime import datetime
from video_downloader import VideoDownloader
from secretary_exceptions import *
from classifier import MessageClassifier
from representations import write_html


DIGEST_DIR = "digest"

def handle(msg):
    global storage
    global bot
    global video_hostings
    global video_download_queue
    global video_downloader_thread
    content_type, chat_type, chat_id = telepot.glance(msg)
    print content_type, chat_type, chat_id

    if content_type != 'text': return
    if msg['text'].strip().lower() == '/digest':
        classes = storage.digest(chat_id, MessageClassifier())
        filename = DIGEST_DIR + "/" + "-".join(str(datetime.utcnow()).split()) + ".html"
        write_html(classes, filename)
        bot.sendChatAction(chat_id, 'upload_document')
        bot.sendDocument(chat_id, open(filename, 'rb'))
    elif msg['text'].strip().lower() == '/pause':
        video_downloader_thread.pause()
    elif msg['text'].strip().lower() == '/resume':
        video_downloader_thread.resume()
    elif urlparse(msg['text']).netloc.lower().replace("www.", "") in video_hostings:
        # TODO: We want to store the url to the DB as well, because the download
        # process can be interrupted and we'll need to re-download.
        # One design is Downloader asking the Storage.
        video_download_queue.put(msg['text'])
    else:
        storage.store_message(msg)

video_hostings = ["youtu.be", "youtube.com"]
video_download_queue = Queue()
video_downloader_thread = VideoDownloader(video_download_queue)
video_downloader_thread.start()
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
