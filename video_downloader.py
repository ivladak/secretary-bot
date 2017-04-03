#!/usr/bin/python
from __future__ import unicode_literals
from controllable_threads import *
import youtube_dl
import Queue
import configuration

class VideoDownloader(PausableThread):
    """VideoDownloader class.

    VideoDownloader downloads videos one by one in a separate thread.
    (In current design it does not spawn a thread for each video right away,
    rather it waits for a download to finish before starting the next.)

    It offers "pause downloading" and "resume downloading" functionality.
    The motivation behind it is to

    A location in the file system to download into will be read from
    a config file (TODO: for now it is hardcoded).
    """
    def __init__(self, download_queue, finished_queue):
        PausableThread.__init__(self)
        self._queue = download_queue
        self._spawned = None
        self._finished_queue = finished_queue

    def _start_download(self, url):
        self._spawned = DownloaderThread([url], self._finished_queue)
        self._spawned.start()

    def run(self):
        while True:
            while not self.paused():
                if self._spawned:
                    # Only allow one download at a time.
                    self._spawned.join(timeout=0.3)
                    if (self._spawned.is_alive()):
                        continue
                    else:
                        self._spawned = None
                try:
                    url = self._queue.get(block=True, timeout=0.3)
                    self._start_download(url)
                except Queue.Empty:
                    pass
                
            if self._spawned:
                self._spawned.stop()
            self.wait_for_resume()

class DownloaderThread(StoppableThread):
    """DownloaderThread class.

    Effectively it's a wrapper-thread around youtube-dl library's downloading
    functionality, which can be stopped (killed) at request.
    """

    def __init__(self, url_list, finished_queue):
        StoppableThread.__init__(self)
        self._url_list = url_list
        self._queue = finished_queue
        dirpath = configuration.get("video_download_dir")
        # youtube-dl templates are documented here:
        # https://github.com/rg3/youtube-dl/blob/master/README.md#output-template.
        ydl_options = {'outtmpl': dirpath + '/%(title)s.%(ext)s',
                       'format': 'mp4/flv/3gp'}

        self._ydl = youtube_dl.YoutubeDL(ydl_options)

        def _raise_hook(status):
            # Check for the stopped condition from the hook using the captured
            # method. Terminate the thread via raising an exception.
            if self.stopped():
                raise Exception("Downloader thread has been stopped.")
            # Check 
            if status['status'] == 'finished':
                self._queue.put(self._url_list[0])

        self._ydl.add_progress_hook(_raise_hook)

    def run(self):
        self._ydl.download(self._url_list)
