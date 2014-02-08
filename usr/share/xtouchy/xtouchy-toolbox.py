#!/usr/bin/env python3
from tkinter import Tk, ttk
import os
import time
import configparser
import argparse

current_rotation = 0 #assuming is bad, and this is no exception

def rotate(direction, window):
    global current_rotation
    if direction == 0:
        return
    current_rotation += direction
    if current_rotation > 3:
        current_rotation -= 4
    elif current_rotation < 0:
        current_rotation += 4
    print("current_rotation: " + str(current_rotation))
    os.system("xrandr --screen 0 -o " + str(current_rotation))
    #0 = normal, 1 = left, 2 = inverted, 3 = right
    if "tablet_name" in settings["wacom"]:
        wacom_id = settings["wacom"]["tablet_name"]
        if current_rotation == 0:
            os.system("xsetwacom --set \"" + wacom_id + "\" Rotate none")
        elif current_rotation == 1:
            os.system("xsetwacom --set \"" + wacom_id + "\" Rotate ccw")
        elif current_rotation == 2:
            os.system("xsetwacom --set \"" + wacom_id + "\" Rotate half")
        elif current_rotation == 3:
            os.system("xsetwacom --set \"" + wacom_id + "\" Rotate cw")
    geom = window.geometry().split("+")
    window.geometry("+" + geom[2] + "+" + geom[1])

def move(event, window):
    if (current_rotation == 1) or (current_rotation == 3):
        #Tk bug 3141377: [winfo screenwidth/height] fail to track resolution changes
        #Feel free to remove this entire if/else part if they fix their shit.
        width = window.winfo_screenheight()
        height = window.winfo_screenwidth()
    else:
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
    if (event.x_root + window.winfo_height() > width):
        event.x_root = width - window.winfo_height()
    if (event.y_root + window.winfo_width() > height):
        event.y_root = height - window.winfo_width()
    moveto = "+" + str(event.x_root) + "+" + str(event.y_root)
    window.geometry(moveto)

def move_vkeyboard(event, window):
    print(event.x)
    if (event.x > int(settings["gui"]["btn_dims"])):
        print("Make KBD right") 
    elif (event.x < 0):
        print("Make KBD left")

def reset_and_exit(window):
    if settings["gui"]["reset_rotation"] == 1:
        rotate(0, window)
    exit()

def open_main():
    btn_dims = int(settings["gui"]["btn_dims"])
    _xt_root = Tk()
    if settings["gui"]["bypass_wm"] == "1":
        _xt_root.overrideredirect(1)
    _xt_root.title("Xtouchy Toolbox")
    _xt_root.maxsize(btn_dims*3, btn_dims*3)
    root_frame = ttk.Frame(_xt_root, padding="0 0 0 0", width=btn_dims*3, height=btn_dims*3)
    root_frame.grid(column=1, row=0, sticky=("N", "W", "E", "S"))
    #Screen orientation
    wrkbtn = ttk.Button(root_frame, width=2, text="↑", command=lambda: rotate(0, _xt_root))
    wrkbtn.place(x=btn_dims, y=0, width=btn_dims, height=btn_dims)
    wrkbtn = ttk.Button(root_frame, width=2, text="↓", command=lambda: rotate(2, _xt_root))
    wrkbtn.place(x=btn_dims, y=btn_dims*2, width=btn_dims, height=btn_dims)
    wrkbtn = ttk.Button(root_frame, width=2, text="←", command=lambda: rotate(1, _xt_root))
    wrkbtn.place(x=0, y=btn_dims, width=btn_dims, height=btn_dims)
    wrkbtn = ttk.Button(root_frame, width=2, text="→", command=lambda: rotate(3, _xt_root))
    wrkbtn.place(x=btn_dims*2, y=btn_dims, width=btn_dims, height=btn_dims)
    #Close/Move button
    mvbtn = ttk.Button(root_frame, width=2, text="⇱")
    mvbtn.bind("<B1-Motion>", lambda x: move(x, _xt_root))
    mvbtn.place(x=0, y=0, width=btn_dims, height=btn_dims)
    ttk.Button(root_frame, width=2, text="X", command=lambda: reset_and_exit(_xt_root)).place(x=btn_dims*2, y=0, width=btn_dims, height=btn_dims)
    #Toggle virtual keyboard
    tvkbtn = ttk.Button(root_frame, width=2, text="K")
    tvkbtn.bind("<B1-Motion>", lambda x: move_vkeyboard(x, _xt_root))
    tvkbtn.place(x=0, y=btn_dims*2, width=btn_dims, height=btn_dims)
    _xt_root.mainloop()

if __name__ == "__main__":
    global settings
    settings = configparser.ConfigParser()
    settings.read('/etc/xtouchy.conf')
    open_main()
