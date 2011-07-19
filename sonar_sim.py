#!/bin/python
from sympy import intersection
from sympy.geometry import Segment, Point
from math import sqrt, cos, sin, radians
from shapely import *
from shapely.geometry import LineString
from Tkinter import *
import time

class particle:

    def __init__(self):
        self.loc = (0,0)
        self.wt = 0
        

class sonar:

    def __init__(self, rng, step, loc, map_):
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through
        self.initial_angle = 0 # Where the first pulse is directed from
        self.map = map_ # Map to use the sonar in
        self.loc = loc # The starting position of the sonar in the map in computer coords
        self.current_angle = self.initial_angle

    def reset(self):
        self.ranges = []
        self.scan_lines = []
        self.intersection_points = []
        self.current_angle = self.initial_angle
        
    def get_ranges(self):
        self.reset()
        for i in [x * self.step for x in map(lambda x:x+1, range(360/self.step))]:
            #print self.current_angle
            if self.current_angle > self.initial_angle + self.angle_range:
                break
            ln = self.get_scan_line()
            intersect = self.get_intersect_point(ln)
            self.current_angle += self.step

    def get_intersect_point(self, scan_line):
        for line in self.map.lines:
            print 'y'
            #print line, scan_line
            #print intersection(line, scan_line)

    def point_distance(self, sonar_loc, intersect):
        print 'not implemented'

    def get_scan_line(self):
        ln = Segment(Point(self.loc[0],self.loc[1]), self.point_at_angle(self.current_angle))
        self.scan_lines.append(ln)
        return ln
       
    def point_at_angle(self, degrees):
        # (x', y') = (x + r cos a, y + r sin a)
        # x,y = centre point, r = radius, a = angle
        return Point(self.loc[0] + (self.max_range * cos(radians(degrees))), self.loc[1] + (self.max_range * sin(radians(degrees))))

class map_:
    # For the purposes of the simulation, each increment of 1 in the
    # coordinate space represents 10cm. i.e. (20,5) is 2m from the
    # origin in the x direction and 50cm from the origin in the y
    # direction.

    def __init__(self):
        self.lines = []
    
    def __repr__(self):
        rep = ""
        for line in self.lines:
            rep += str(line) + "\n"
        return rep
        
    def add_line(self, line):
        self.lines.append(line)

def angle_point_test(start, step):
    master = Tk()
    w = Canvas(master)
    w.pack()
    start_angle = start
    pt = sonar.point_at_angle(start_angle)
    w.create_oval(pt[0], pt[1], pt[0] + 2, pt[1] + 2, fill='red')
    for i in [x * step for x in map(lambda x:x+1, range(360/step))]:
        if i > 265:
            break
        pt = sonar.point_at_angle(start_angle+i)
        draw_point(w, pt)
    w.mainloop()

def scan_line_test():
    sonar.get_ranges()
    master = Tk()
    w = Canvas(master)
    w.pack()
    for line in sonar.scan_lines:
        draw_line(w, line)
    w.mainloop()

def draw_line(canvas, line):
    canvas.create_line(line[0][0], line[0][1], line[1][0], line[1][1])

def draw_point(canvas, point):
    canvas.create_oval(point[0], point[1], point[0] + 2, point[1] + 2)

if __name__ == '__main__':
    simple_map = map_()
    simple_map.add_line(Segment(Point(2,2), Point(2,40)))
    simple_map.add_line(Segment(Point(2,2), Point(40,2)))
    simple_map.add_line(Segment(Point(40,2), Point(40,40)))
    simple_map.add_line(Segment(Point(2,40), Point(40,40)))
    sonar = sonar(50, 25, Point(20,20), simple_map)
    
    sonar.get_ranges()
    
    a = LineString([(2,2),(2,40)])
    b = LineString([(2,2),(40,2)])
    c = LineString([(40,2),(40,40)])
    d = LineString([(2,40),(40,40)])
    
    lines = [a,b,c,d]
    ed = []
    for s_line in sonar.scan_lines:
        ed.append(LineString([(s_line[0][0], s_line[0][1]),(s_line[1][0], s_line[1][1])]))

    for e in ed:
        print 'new line'
        for line in lines:
            print e.intersection(line)


    #master = Tk()
    #w = Canvas(master)
    #w.pack()
    for point in sonar.intersection_points:
        print point
#    w.mainloop()
