import numpy as np
import cv2
import time
import concurrent.futures
import win32com.client as comclt
from directkeys import PressKey, W, A, S, D

from modules.get_tasks import get_tasks
from modules.get_window import get_window_dimensions, watch_window
from modules.get_location import get_location

white_upper = np.array([0, 0, 255])
white_lower = np.array([0, 0, 0])


class AmongUsBot():
    """Class used to get the dimensions and that of the Among Us
    window
    """
    def __init__(self):
        window_dimensions, window_handle = get_window_dimensions()

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
                    get_task_panel = executor.submit(get_tasks, screen)
                    tasks = get_task_panel.result()
                    print(f'Player\'s current tasks: {", ".join(tasks)}')

                task_time = 10

            task_time -= 1
            position_time -= 1

            print("Took {} miliseconds".format((time.time()-last_time)*1000))
            last_time = time.time()

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()


if __name__ == '__main__':
    AmongUsBot()
