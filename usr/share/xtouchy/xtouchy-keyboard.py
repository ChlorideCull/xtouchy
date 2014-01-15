#!/usr/bin/env python3
from tkinter import Tk, ttk

def open_main():
    #Imitate main program, for later incorporation
    global _xt_root
    _xt_root = Tk()
    _xt_root.title("Xtouchy Keyboard Test")
    root_frame = ttk.Frame(_xt_root, padding="0 0 0 0", width=81, height=75)
    root_frame.grid(column=1, row=0, sticky=("N", "W", "E", "S"))
    ttk.Button(root_frame, width=2, text="K").grid(column=0, row=0, sticky=("N", "W", "E", "S"))
    _xt_root.mainloop()

open_main()
