import cv2


def colour_filter(screen, colour_upper, colour_lower):
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, colour_lower, colour_upper)
    res = cv2.bitwise_and(screen, screen, mask=mask)

    return res