import concurrent.futures
import time

import cv2
import numpy as np
import win32com.client as comclt

from directkeys import A, D, PressKey, S, W
from modules.get_location import get_location
from modules.get_tasks import get_tasks
from modules.get_window import get_window_dimensions, watch_window
from modules.config import config

class AmongUsBot():
    """Class used to get the dimensions and that of the Among Us
    window
    """
    def __init__(self):
        settings = config()
        self.start(settings)

    def start(self, settings):
        _, window_handle = get_window_dimensions()

        window_dimensions = settings['dimensions']
        task_coords = [settings['top_left_task'][0], settings['top_left_task'][1],
                       settings['bot_right_task'][0] - settings['top_left_task'][0],
                       settings['bot_right_task'][1] - settings['top_left_task'][1]]

        last_time = time.time()
        wsh = comclt.Dispatch("WScript.Shell")

        task_time = 0
        position_time = 0

        print("Starting to watch game...")

        while True:
            with concurrent.futures.ThreadPoolExecutor() as window_getter:
                future = window_getter.submit(watch_window,
                                              window_dimensions,
                                              window_handle)
                screen = future.result()

                if position_time == 0:
                    room = get_location(screen)
                    if room:
                        print(f'Player is in {room[0]}')

                    position_time = 10

            if task_time == 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    get_task_panel = executor.submit(get_tasks, screen,
                                                     task_coords)
                    tasks = get_task_panel.result()
                    print(f'Player\'s current tasks: {", ".join(tasks)}')

                task_time = 10

            task_time -= 1
            position_time -= 1

            # print("Took {} miliseconds".format((time.time()-last_time)*1000))
            last_time = time.time()

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()


if __name__ == '__main__':
    AmongUsBot()
