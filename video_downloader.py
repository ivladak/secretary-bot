#!/usr/bin/python
from __future__ import unicode_literals
import youtube_dl
import threading
import Queue
import configuration


class StoppableThread(threading.Thread):
    """Thread class with a stop() method.
    The thread itself has to check regularly for the stopped() condition."""

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.daemon = True

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class PausableThread(threading.Thread):
    """Thread class with pause() and resume() methods.
    The thread itself has to check regularly for the paused() condition."""

    def __init__(self):
        threading.Thread.__init__(self)
        self._pause = threading.Event()
        self._resume = threading.Event()
        self.daemon = True

    def pause(self):
        self._resume.clear()
        self._pause.set()

    def resume(self):
        self._pause.clear()
        self._resume.set()

    def paused(self):
        return self._pause.isSet()

    def wait_for_resume(self):
        self._resume.wait()


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
    def __init__(self, download_queue):
        PausableThread.__init__(self)
        self._queue = download_queue
        self._spawned = None

    def _start_download(self, url):
        self._spawned = DownloaderThread([url])
        self._spawned.start()

    def run(self):
        while True:
            while not self.paused():
                if self._spawned:
                    # Only allow one download at a time.
                    self._spawned.join(timeout=0.3)
                    if (self._spawned.is_alive()):
                        continue
                try:
                    url = self._queue.get(block=True, timeout=0.3)
                    self._start_download(url)
                except Queue.Empty:
                    pass
            self._spawned.stop()
            self.wait_for_resume()


class DownloaderThread(StoppableThread):
    """DownloaderThread class.

    Effectively it's a wrapper-thread around youtube-dl library's downloading
    functionality, which can be stopped (killed) at request.
    """

    def __init__(self, url_list):
        StoppableThread.__init__(self)
        self._url_list = url_list
        dirpath = configuration.get("video_download_dir")
        # youtube-dl templates are documented here:
        # https://github.com/rg3/youtube-dl/blob/master/README.md#output-template
        ydl_options = {'outtmpl': dirpath + '/%(title)s.%(ext)s'}
        self._ydl = youtube_dl.YoutubeDL(ydl_options)

        def _raise_hook(status):
            # Check for the stopped condition from the hook using the captured
            # method. Terminate the thread via raising an exception.
            if self.stopped():
                raise Exception("Downloader thread has been stopped.")

        self._ydl.add_progress_hook(_raise_hook)

    def run(self):
        self._ydl.download(self._url_list)