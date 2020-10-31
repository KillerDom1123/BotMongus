from PIL import ImageGrab
import numpy as np
import win32gui
import cv2
import time
import concurrent.futures
import pytesseract
import re
import win32com.client as comclt
from directkeys import PressKey, W, A, S, D
from difflib import get_close_matches

list_of_tasks = [
    'admin swipe card',
    'upper engine align engine output',
    'electrical divert power to communications',
    'electrical calibrate distributor',
    'weapons clear asteroids',
    'navigation download data'
]

list_of_rooms = [
    'storage',
    'cafeteria',
    'upper engine',
    'reactor',
    'lower engine',
    'medbay',
    'electrical',
    'weapons',
    'navigation',
    'shields',
    'o2',
    'admin',
    'communications',
    'security'
]

white_upper = np.array([0, 0, 255])
white_lower = np.array([0, 0, 0])


class AmongUsBot():
    """Class used to get the dimensions and that of the Among Us
    window
    """
    def __init__(self):
        window_dimensions, window_handle = self.get_window_dimensions()

        last_time = time.time()
        wsh = comclt.Dispatch("WScript.Shell")

        task_time = 0
        position_time = 0

        print("Starting to watch game...")

        while True:
            with concurrent.futures.ThreadPoolExecutor() as window_getter:
                future = window_getter.submit(self.watch_window,
                                              window_dimensions,
                                              window_handle)
                screen = future.result()

                if position_time == 0:
                    room = self.get_location(screen)
                    if room:
                        print(f'Player is in {room[0]}')

                    position_time = 10

            if task_time == 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    get_task_panel = executor.submit(self.get_tasks, screen)
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
            cv2.waitKey(5000)

    def watch_window(self, window_dimensions, window_handle):

        (left_x, top_y,
         right_x, bottom_y) = (window_dimensions[0], window_dimensions[1],
                               window_dimensions[2], window_dimensions[3])

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
        task_panel = self.colour_filter(task_panel, white_upper, white_lower)

        gray = cv2.cvtColor(task_panel, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        tasks = pytesseract.image_to_string(thresh)
        split_tasks = [re.sub('[^A-Za-z]+', ' ', task.lower())
                       for task in tasks.split('\n')]

        list_of_current_tasks = []

        for task_line in split_tasks:
            if re.sub(r"\s+", "", task_line, flags=re.UNICODE):
                match = get_close_matches(task_line, list_of_tasks)
                if match:
                    list_of_current_tasks.append(match[0])

        list_of_current_tasks = list(filter(None, list_of_current_tasks))
        return list_of_current_tasks

    def get_position_on_map(self, screen):
        img_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('BotMongus\icon.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        return loc
        # cv2.imshow('deee',screen)

    def get_location(self, screen):
        x, y, w, h = (674, 950, 590, 150)
        room_name_screen = screen[y:y+h, x:x+w]
        room_name_screen = self.colour_filter(room_name_screen,
                                              white_upper,
                                              white_lower)

        gray = cv2.cvtColor(room_name_screen, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        room = pytesseract.image_to_string(thresh)

        return get_close_matches(room.lower(), list_of_rooms)

    def colour_filter(self, screen, colour_upper, colour_lower):
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, colour_lower, colour_upper)
        res = cv2.bitwise_and(screen, screen, mask=mask)

        return res


if  __name__ == '__main__':
    AmongUsBot()
