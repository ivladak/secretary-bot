import threading

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


