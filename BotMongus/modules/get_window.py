import numpy as np
import win32gui
from PIL import ImageGrab


def get_window_dimensions():
    print('Getting window...')

    foreground_window = win32gui.GetForegroundWindow()
    # win32gui.SetForegroundWindow(among_us_window)
    window_dimensions = win32gui.GetWindowRect(foreground_window)

    return window_dimensions, foreground_window


def watch_window(window_dimensions, window_handle):
    (left_x, top_y,
     right_x, bottom_y) = (window_dimensions[0], window_dimensions[1],
                           window_dimensions[2], window_dimensions[3])

    while True:
        screen = np.array(ImageGrab.grab(bbox = (left_x, top_y,
                                                    right_x, bottom_y)))

        return screen
