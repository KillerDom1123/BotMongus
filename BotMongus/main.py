from PIL import ImageGrab
import numpy as np
from numpy.lib.shape_base import split
import win32gui
import cv2
import time
import concurrent.futures
import pytesseract
import re
import win32com.client as comclt
from directkeys import PressKey, W, A, S, D

list_of_tasks = [
    'admin swipe card',
    'upper engine align engine output',
    'electrical divert power to communications',
    'electrical calibrate distributor'
]


class AmongUsBot():
    """Class used to get the dimensions and that of the Among Us
    window
    """
    def __init__(self):
        window_dimensions, window_handle = self.get_window_dimensions()

        last_time = time.time()
        wsh= comclt.Dispatch("WScript.Shell")

        task_time = 0

        while True:
            with concurrent.futures.ThreadPoolExecutor() as window_getter:
                future = window_getter.submit(self.watch_window,
                                              window_dimensions,
                                              window_handle)
                screen = future.result()

            if task_time == 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    get_task_panel = executor.submit(self.get_tasks, screen)
                    tasks = get_task_panel.result()

                task_time = 10

            task_time -= 1

            print("Took {} miliseconds".format((time.time()-last_time)*1000))
            last_time = time.time()


            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()

    def get_window_dimensions(self):
        print('Getting window...')

        while True:
            if win32gui.FindWindow(None, r'Among Us'):
                print('Among Us window found...')

                among_us_window = win32gui.FindWindow(None, r'Among Us')
                print(among_us_window)
                # win32gui.SetForegroundWindow(among_us_window)
                window_dimensions = win32gui.GetWindowRect(among_us_window)

                print(f'Window dimensions: {window_dimensions}')

                return window_dimensions, among_us_window

            print("No window found. Trying again in 5 seconds...")
            time.sleep(5)

    def watch_window(self, window_dimensions, window_handle):
        print("Starting to watch game...")


        left_x, top_y, right_x, bottom_y = window_dimensions[0], window_dimensions[1], window_dimensions[2], window_dimensions[3]

        while True:
            if win32gui.GetForegroundWindow() == window_handle:
                screen = np.array(ImageGrab.grab(bbox=(left_x, top_y,
                                                   right_x, bottom_y)))

                return screen

            else:
                print("Among Us window is not foreground. Waiting 5 seconds")
                cv2.waitKey(5000)

    def get_tasks(self, screen):
        x, y, w, h = (18, 108, 770, 210)
        task_panel = screen[y:y+h, x:x+w]

        gray = cv2.cvtColor(task_panel, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


        tasks = pytesseract.image_to_string(thresh)
        split_tasks = [task for task in tasks.split('\n')]

        list_of_current_tasks = []

        for task_line in split_tasks:
            plain_task = re.sub('[^A-Za-z]+', ' ', task_line.lower())

            split_plain_task = plain_task.split(' ')

            for text in split_plain_task:
                matching = [s for s in list_of_tasks if text in s]

                if len(matching) == 1:
                    list_of_current_tasks.append(matching[0])
                    break

        return list_of_current_tasks

if  __name__ == '__main__':
    AmongUsBot()
