#!usr/bin/python
import os
import sys
from Tkinter import *
import tkFileDialog
import tkMessageBox
import math # REMOVE 


def init():
    global point_list
    global sonar_pos
    global pos_flag
    global mv_flag
    global mv_points
    point_list = []
    mv_points = []
    sonar_pos = None
    pos_flag = 0
    mv_flag = 0
    create_canvas()
   
def create_canvas():
    ms = Tk()
    global canvas

    sv = Button(ms, text='Save map', command=save_map_to_file)
    sv.pack()
    sm = Button(ms, text='Save move', command=save_move_to_file)
    sm.pack()
    sn = Button(ms, text='Sonar pos', command=set_sonar_pos)
    sn.pack()
    mv = Button(ms, text='Movement list', command=create_move_list)
    mv.pack()
    canvas = Canvas(ms, width=800, height=800)
    canvas.pack()
    canvas.bind("<Button-1>", m1down)
    canvas.mainloop()

def set_sonar_pos():
    global pos_flag
    pos_flag = 1
    
def create_move_list():
    global mv_flag
    mv_flag = 1 if mv_flag is 0 else 0

def save_map_to_file():
    if not sonar_pos:
        tkMessageBox.showwarning("Error", "You must define a sonar location for the map.")
        return
    f = tkFileDialog.asksaveasfile(defaultextension='.map')
    f.write('%d %d '%(sonar_pos))
    for val in point_list:
        f.write(str(val) + ' ')
    f.close()

def save_move_to_file():
    print 'implement'
    if not mv_points:
        tkMessageBox.showwarning("Error", "You haven\'t made a move sequence.")
        return
    f = tkFileDialog.asksaveasfile(defaultextension='.mv')
    for val in mv_points:
        f.write(str(val) + ' ')
    f.close()

def m1down(event):
    # Might be nice to extend this to make it so that if you click
    # close to another point (say within 5 units), then the point
    # added is the same as the one that is close.
    global pos_flag
    global mv_flag
    if pos_flag:
        pos_flag = 0
        global sonar_pos 
        sonar_pos = (event.x, event.y)
        print 'Setting sonar position to ' + str(sonar_pos)
    elif mv_flag:
        if mv_flag is 1:
            mv_points.extend([event.x, event.y])
            #mv_flag = 2
        #elif mv_flag = 2:
            
    else:
        point_list.extend([event.x, event.y])
        if len(point_list) % 4 is 0:
            canvas.create_line(*point_list[-4:])
    
if __name__ == '__main__':
    init()
