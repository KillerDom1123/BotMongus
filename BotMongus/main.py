from PIL import ImageGrab
import numpy as np
import win32gui
import cv2
import time
import concurrent.futures

class AmongUsBot():
    """Class used to get the dimensions and that of the Among Us
    window
    """
    def __init__(self):
        window_dimensions, window_handle = self.get_window_dimensions()

        self.watch_window(window_dimensions, window_handle)

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
        last_time = time.time()

        left_x, top_y, right_x, bottom_y = window_dimensions[0], window_dimensions[1], window_dimensions[2], window_dimensions[3]

        while True:
            if win32gui.GetForegroundWindow() == window_handle:
                screen = np.array(ImageGrab.grab(bbox=(left_x, top_y,
                                                   right_x, bottom_y)))

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    get_task_panel = executor.submit(self.get_tasks, screen)
                    return_value = get_task_panel.result()

                cv2.imshow('Recorded Image', screen)
                cv2.imshow('tasks', return_value)
                print("Took {} miliseconds".format((time.time()-last_time)*1000))
                last_time = time.time()


                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    exit()

            else:
                print("Among Us window is not foreground. Waiting 5 seconds")
                key = cv2.waitKey(5000)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    exit()

                last_time = time.time()

    def get_tasks(self, screen):
        x, y, w, h = (18, 108, 770, 210)

        task_panel = screen[y:y+h, x:x+w]
        # task_panel = cv2.resize(screen, None, fx=)
        return task_panel

if  __name__ == '__main__':
    AmongUsBot()