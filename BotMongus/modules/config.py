import json
import os.path
import time
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilename

import pyautogui

from modules.get_window import get_window_dimensions


def config():
    settings = {}

    if not os.path.exists('config.json'):
        root = tk.Tk()
        # root.withdraw()
        result = tkinter.messagebox.askyesno("Missing config file", "No config file detected. Is it stored elsewhere?")

        if result is True:
            location = askopenfilename(filetypes=(("JSON Files", "*.json"),))

            if location:
                with open(location, 'r') as f:
                    settings = json.load(f)

                    return settings

        print("Starting configuration process")

        while True:
            tkinter.messagebox.showinfo("Configuration 1/0.",
                                        "Open your game and wait 5 seconds.")
            time.sleep(5)

            dimensions, handle = get_window_dimensions()

            print(f"Got dimensions: {dimensions} and handle {handle}")
            result = tkinter.messagebox.askyesno(
                "Configuration Information.",
                f"Got resolution {dimensions[2]}x{dimensions[3]}. Is this correct?")

            if result is True:
                settings['dimensions'] = dimensions
                break

        tkinter.messagebox.showinfo("Configuration 2/0.",
                                    """Move your cursor to the top left of
your task box and wait 5 seconds""")

        time.sleep(5)
        top_left_task = pyautogui.position()
        settings['top_left_task'] = top_left_task

        tkinter.messagebox.showinfo("Configuration 3/0.",
                                    ("""Move your cursor to the bottom right of
your task box and wait 5 seconds"""))

        time.sleep(5)
        bot_right_task = pyautogui.position()
        settings['bot_right_task'] = bot_right_task

        result = tkinter.messagebox.askyesno("Configuration",
                                             f"""Configuration complete. Are these settings correct?
Resolution: {dimensions[2]}x{dimensions[3]}
Top left task bar: {top_left_task[0]}x{top_left_task[1]}
Bottom right task bar: {bot_right_task[0]}x{bot_right_task[1]}""")

        if result is True:
            with open('config.json', 'w') as f:
                json.dump(settings, f)

            root.destroy()

            return settings

        else:
            root.destroy()
            config()

    else:
        with open('config.json', 'r') as f:
            settings = json.load(f)

            return settings
