#!usr/bin/python
import os
import sys
from Tkinter import *

def create_map():
    print 'b'

def create_canvas():
    ms = Tk()
    global canvas
    canvas = Canvas(ms, width=1000, height=1000)
    canvas.pack()
    canvas.mainloop()

if __name__ == '__main__':
    create_canvas()
    create_map()
