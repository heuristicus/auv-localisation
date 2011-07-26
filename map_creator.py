#!usr/bin/python
import os
import sys
from Tkinter import *


def init():
    global point_list
    point_list = []
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
    point_list.extend([event.x, event.y])
    if len(point_list) % 4 is 0:
        canvas.create_line(*point_list[-4:])

if __name__ == '__main__':
    init()
