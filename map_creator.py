#!usr/bin/python
import os
import sys
from Tkinter import *


def init():
    global point_list
    global click_count # messy, but whatever
    point_list = []
    click_count = 0
    create_canvas()
   
def create_map():
    print 'b'

def create_canvas():
    ms = Tk()
    global canvas
    canvas = Canvas(ms, width=1000, height=1000)
    canvas.pack()
    canvas.bind("<Button-1>", m1down)
    ms.after_idle(create_map)
    canvas.mainloop()

def m1down(event):
    global click_count
    click_count = 0 if click_count == 1 else 1
    point_list.extend([event.x, event.y])
    print point_list, click_count

if __name__ == '__main__':
    init()
