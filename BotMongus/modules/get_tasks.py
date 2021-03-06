import re
from difflib import get_close_matches

import cv2
import numpy as np
import pytesseract

from .utils import colour_filter

list_of_tasks = [
    'admin swipe card',
    'upper engine align engine output',
    'electrical divert power to communications',
    'electrical divert power to security',
    'electrical calibrate distributor',
    'weapons clear asteroids',
    'navigation download data',
    'storage fuel engines',
    'o2 clean o2 filter',
    'electrical divert power to navigation',
    'cafeteria empty garbage',
    'navigation stabilize steering',
    'shields prime shields',
    'communications download data'
]

imposter_task = [
    'sabotage and kill everyone',
    'fake tasks'
]

white_upper = np.array([0, 0, 255])
white_lower = np.array([0, 0, 0])


def get_tasks(screen, task_coords):
    x, y, w, h = task_coords
    task_panel = screen[y:y+h, x:x+w]
    task_panel = colour_filter(task_panel, white_upper, white_lower)

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
