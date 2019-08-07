import signal
import threading
import os


class Watchdog():
    def __init__(self):
        self.timeout = self.get_timeout()
        self._t = None

    def do_expire(self):
        os.kill(os.getpid(), signal.SIGTERM)

    def _expire(self):
        print("\nWatchdog expire")
        self.do_expire()

    def start(self):
        if self._t is None:
            self._t = threading.Timer(self.timeout, self._expire)
            self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

    def refresh(self):
        if self._t is not None:
            self.stop()
            self.start()

    def get_timeout(self, default=120):
        file_path = "./watchdog_config.txt"
        while True:
            if os.path.exists(file_path):
                f = open(file_path, "r")
                try:
                    timeout = f.readlines()[0]
                    timeout = int(timeout)
                    f.close()
                    return timeout
                except IndexError:
                    f.close()
                    os.remove(file_path)
                    continue
            else:
                f = open(file_path, "w+")
                f.write(str(default))
                f.close()
                return default
