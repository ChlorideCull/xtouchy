#!/usr/bin/env python3
from tkinter import Tk, ttk
import os
import time
import json
import argparse

current_rotation = 0 #assuming is bad, and this is no exception

def rotate(direction):
    global current_rotation
    current_rotation += direction
    if current_rotation > 3:
        current_rotation -= 4
    elif current_rotation < 0:
        current_rotation += 4
    print("current_rotation: " + str(current_rotation))
    os.system("xrandr --screen 0 -o " + str(current_rotation))
    #0 = normal, 1 = left, 2 = inverted, 3 = right
    if settings["wacom_device_id"] != "":
        wacom_id = settings["wacom_device_id"]
        if current_rotation == 0:
            os.system("xsetwacom --set " + wacom_id + " Rotate none")
        elif current_rotation == 1:
            os.system("xsetwacom --set " + wacom_id + " Rotate ccw")
        elif current_rotation == 2:
            os.system("xsetwacom --set " + wacom_id + " Rotate half")
        elif current_rotation == 3:
            os.system("xsetwacom --set " + wacom_id + " Rotate cw")
    geom = root.geometry().split("+")
    root.geometry("+" + geom[2] + "+" + geom[1])

def move(event, window):
    if (current_rotation == 1) or (current_rotation == 3):
        #Tk bug 3141377: [winfo screenwidth/height] fail to track resolution changes
        #Feel free to remove this entire if/else part if they fix their shit.
        width = window.winfo_screenheight()
        height = window.winfo_screenwidth()
    else:
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
    if (event.x_root + 81 > width):
        event.x_root = width - 81
    if (event.y_root + 75 > height):
        event.y_root = height - 75
    moveto = "+" + str(event.x_root) + "+" + str(event.y_root)
    window.geometry(moveto)

def move_vkeyboard(event):
    print(event.x)
    if (event.x > 27):
        print("Make KBD right") 
    elif (event.x < 0):
        print("Make KBD left")

def open_main():
    global _xt_root
    _xt_root = Tk()
    _xt_root.overrideredirect(1)
    _xt_root.title("Xtouchy Toolbox")
    _xt_root.maxsize(81, 75) #27 height per button, 25 width per button.
    root_frame = ttk.Frame(_xt_root, padding="0 0 0 0", width=81, height=75)
    root_frame.grid(column=1, row=0, sticky=("N", "W", "E", "S"))
    #Screen orientation
    ttk.Button(root_frame, width=2, text="↑", command=lambda: rotate(0)).grid(column=2, row=1, sticky="N")
    ttk.Button(root_frame, width=2, text="↓", command=lambda: rotate(2)).grid(column=2, row=3, sticky="S")
    ttk.Button(root_frame, width=2, text="←", command=lambda: rotate(1)).grid(column=1, row=2, sticky="W")
    ttk.Button(root_frame, width=2, text="→", command=lambda: rotate(3)).grid(column=3, row=2, sticky="E")
    #Close/Move button
    mvbtn = ttk.Button(root_frame, width=2, text="⇱")
    mvbtn.bind("<B1-Motion>", lambda x: move(x, _xt_root))
    mvbtn.grid(column=1, row=1, sticky=("N", "W"))
    ttk.Button(root_frame, width=2, text="X", command=exit).grid(column=3, row=1, sticky=("N", "E"))
    #Toggle virtual keyboard
    tvkbtn = ttk.Button(root_frame, width=2, text="K")
    tvkbtn.bind("<B1-Motion>", move_vkeyboard)
    tvkbtn.grid(column=1, row=3, sticky=("S", "W"))
    _xt_root.mainloop()

if __name__ == "__main__":
    global settings
    parser = argparse.ArgumentParser(description="Xtouchy Toolbox - an Tk TabletPC toolbox")
    parser.add_argument("-s", "--set", dest="setoption", nargs=2, help="Sets the option [1] to the value of [2]")
    parser.add_argument("-g", "--get", dest="getoption", nargs=1, help="Gets the option [1]")
    parser.add_argument("-l", "--list", dest="listoption", action="store_true", help="Lists all options")
    args = parser.parse_args()
    settings_file_handle = open("/etc/xtouchy.json", mode="r")
    settings = json.load(settings_file_handle)
    settings_file_handle.close()
    if args.setoption != None:
        settings[args.setoption[0]] = args.setoption[1]
        try:
            settings_file_handle = open("/etc/xtouchy.json", mode="w")
        except PermissionError:
            print("Not sufficient permissions to write, did you forget to sudo?")
            exit(2)
        json.dump(settings, settings_file_handle)
        settings_file_handle.close()
        exit(0)
    elif args.getoption != None:
        if args.getoption in settings:
            print(settings[args.getoption])
            exit(0)
        else:
            print("No such variable")
            exit(1)
    elif args.listoption:
        for x in settings:
            print(x, ":", settings[x])
        exit(0)
    else:
        open_main()
