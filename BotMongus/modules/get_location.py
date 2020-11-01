from difflib import get_close_matches

import cv2
import numpy as np
import pytesseract

from .utils import colour_filter

white_upper = np.array([0, 0, 255])
white_lower = np.array([0, 0, 0])


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


def get_position_on_map(screen):
    img_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('BotMongus\icon.png', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    return loc
    # cv2.imshow('deee',screen)


def get_location(screen):
    x, y, w, h = (674, 950, 590, 150)
    room_name_screen = screen[y:y+h, x:x+w]
    room_name_screen = colour_filter(room_name_screen,
                                     white_upper,
                                     white_lower)

    gray = cv2.cvtColor(room_name_screen, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    room = pytesseract.image_to_string(thresh)

    return get_close_matches(room.lower(), list_of_rooms)
