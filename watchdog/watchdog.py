"""
The Watchdog module created a generic watchdog implementation to handle
the program timeout.
Once the instance is created it is updated againt everey user activity.
Once expired, the program is terminated.
"""

import signal
import threading
import os


class Watchdog:
    """
    Watchdog class that handled the program timeout
    """
    def __init__(self):
        self.timeout = self.get_timeout()
        self._t = None

    @staticmethod
    def do_expire():
        """
        Closes the program
        :return: None
        """
        os.kill(os.getpid(), signal.SIGTERM)

    def _expire(self):
        """
        Expires the program
        :return: None
        """
        print("\nWatchdog expire")
        self.do_expire()

    def start(self):
        """
        Start monitoring the user actions
        :return: None
        """
        if self._t is None:
            self._t = threading.Timer(self.timeout, self._expire)
            self._t.start()

    def stop(self):
        """
        Stops the monitoring
        :return: None
        """
        if self._t is not None:
            self._t.cancel()
            self._t = None

    def refresh(self):
        """
        Once the watchdog is refreshed, it restart itself
        :return:
        """
        if self._t is not None:
            self.stop()
            self.start()

    @staticmethod
    def get_timeout(default=120):
        """
        Get the timout setup from config
        :param default:
        :return: timeout in seconds
        """
        file_path = "./watchdog_config.txt"
        while True:
            if os.path.exists(file_path):
                config_file = open(file_path, "r")
                try:
                    timeout = config_file.readlines()[0]
                    timeout = int(timeout)
                    config_file.close()
                    return timeout
                except IndexError:
                    config_file.close()
                    os.remove(file_path)
                    continue
            else:
                config_file = open(file_path, "w+")
                config_file.write(str(default))
                config_file.close()
                return default
