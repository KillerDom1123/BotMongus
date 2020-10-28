from threading import Thread
import cv2
import sys
import os
import subprocess
import re

class BotMongus():
    """Among Us Bot class

    Gets the window and starts the process
    """
    def __init__(self):
        print("Starting bot...")
        while True:
            name = self.get_active_window_title()
            print(name)

    def get_active_window_title(self):
        root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
        stdout, _ = root.communicate()
        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
        if m is not None:
            window_id = m.group(1)
            window = subprocess.Popen(['xprop', '-id', window_id,
                                       'WM_NAME'],
                                      stdout=subprocess.PIPE)
            stdout, _ = window.communicate()
        else:
            return None

        print(stdout)

        match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)

        if match is not None:
            return match.group("name").strip(b'"')

        return None


if __name__ == "__main__":
    BotMongus()