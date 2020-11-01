import time
import sys
import pyautogui
import win32api
state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

while True:
    a = win32api.GetKeyState(0x01)

    if a != state_left:  # Button state changed
        state_left = a
        print(a)
        if a < 0:
            BOTRIGHT = pyautogui.position()
            print("Mouse At {}".format(BOTRIGHT))
            break