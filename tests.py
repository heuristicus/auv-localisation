#!/usr/bin/python
from Tkinter import *
from sonar_sim import *


def angle_point_test(start, step):
    create_canvas()
    start_angle = start
    pt = s.point_at_angle(start_angle)
    canvas.create_oval(pt.x, pt.y, pt.x + 2, pt.y + 2, fill='red')
    for i in [x * step for x in map(lambda x:x+1, range(360/step))]:
        if i > 265:
            break
        pt = s.point_at_angle(start_angle+i)
        draw_point(canvas, pt)
#   canvas.mainloop()

def scan_line_test():
    s.get_ranges()
    create_canvas()
    for line in s.scan_lines:
        draw_line(canvas, line)
    #canvas.mainloop()

def intersection_point_test():
    s.get_ranges()
    create_canvas()
    for line in s.scan_lines:
        draw_line(canvas,line)
    for pt in s.intersection_points:
        draw_point(canvas,pt)
    simple_map.draw(canvas)
    #canvas.mainloop()

def create_canvas():
    global canvas
    master = Tk()
    canvas = Canvas(master)
    canvas.pack()

if __name__ == '__main__':
    global s
    simple_map = map_()
    simple_map.add_line(LineString([(2,2),(2,40)]))
    simple_map.add_line(LineString([(2,2),(40,2)]))
    simple_map.add_line(LineString([(40,2),(40,40)]))
    simple_map.add_line(LineString([(2,40),(40,40)]))
    
    s = sonar(50, 25, Point(20,20), simple_map, [])
    angle_point_test(10,10)
    scan_line_test()
    intersection_point_test()
    
    canvas.mainloop()
