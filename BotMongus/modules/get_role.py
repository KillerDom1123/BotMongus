import re
from difflib import get_close_matches

import cv2
import numpy as np
import pytesseract

from .utils import colour_filter

imposter_task = [
    'sabotage and kill everyone',
]

red_upper = np.array([120, 255, 255])
red_lower = np.array([120, 200, 100])


def get_role(screen, task_coords):
    x, y, w, h = task_coords
    imposter_panel = screen[y:y+h, x:x+w]
    imposter_panel = colour_filter(imposter_panel, red_upper, red_lower)

    gray = cv2.cvtColor(imposter_panel, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    role = pytesseract.image_to_string(thresh)

    if len(get_close_matches(role.lower(), imposter_task)) > 0:
        return True

    return False
