import threading
import subprocess
from secretary_exceptions import MeditationException
from time import sleep


class MeditationState:
    def __init__(self):
        self._meditating = False

    def start_meditating(self):
        self._meditating = True

    def stop_meditating(self):
        self._meditating = False

    def is_meditating(self):
        return self._meditating


class MeditationManager:
    """MeditationManager class.

    Meditation manager has a state indicating if a meditation process
    is going on and makes it impossible to start a meditation session
    if one is already running. The need for it is obvious, since a meditation
    session has arbitrary (user specified) length and it starts and ends with
    a gong sound, thus nested meditation sessions make no sense.
    """
    def __init__(self):
        self.state = MeditationState()

    def meditate(self, time=None):
        """Try to meditate time minutes (or default if not specified).

        Raises an exception if time is unintelligible or if a meditation
        session is already running.
        """
        if self.state.is_meditating():
            raise MeditationException("Already meditating")
        thread = MeditationThread(self.state, self._int_time(time))
        # 'Locking' and checking always happens in the main thread.
        try:
            self.state.start_meditating()
            thread.start()
        except:
            self.state.stop_meditating()

    def _int_time(self, time):
        if time == None:
            return MeditationManager.meditation_time_default
        try:
            int_time = int(time)
        except:
            raise MeditationException("Non-integer time specified")
        if (int_time < MeditationManager.meditation_time_min or
            int_time > MeditationManager.meditation_time_max):
            raise MeditationException("Meditation time out of bounds")
        return int_time

    meditation_time_default = 30
    meditation_time_min = 1
    meditation_time_max = 60 * 24 * 31


class MeditationThread(threading.Thread):
    def __init__(self, state, time):
        threading.Thread.__init__(self)
        self.state = state
        self.time = time

    def run(self):
        """Initiate a self.time minutes long meditation session."""
        play_gong_args = ["aplay", "sound/gong.wav"]
        subprocess.call(play_gong_args)
        sleep(self.time * 60)
        subprocess.call(play_gong_args)
        self.state.stop_meditating()
