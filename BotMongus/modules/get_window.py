import win32gui
from PIL import ImageGrab
import cv2
import numpy as np


def get_window_dimensions():
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


def watch_window(window_dimensions, window_handle):
    (left_x, top_y,
     right_x, bottom_y) = (window_dimensions[0], window_dimensions[1],
                           window_dimensions[2], window_dimensions[3])

    while True:
        if win32gui.GetForegroundWindow() == window_handle:
            screen = np.array(ImageGrab.grab(bbox = (left_x, top_y,
                                                     right_x, bottom_y)))

            return screen

        else:
            print("Among Us window is not foreground. Waiting 5 seconds")