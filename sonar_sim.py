#!/bin/python
from sympy import intersection
from sympy.geometry import Segment, Point
from math import sqrt, cos, sin, radians
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

    def get_ranges(self):
        print 'not implemented'

    def get_intersect_point(self, scan_line):
        print 'not implemented'

    def point_distance(self, sonar_loc, intersect):
        print 'not implemented'

    def get_scan_line(self):
        print 'not implemented'
       
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

if __name__ == '__main__':
    simple_map = map_()
    simple_map.add_line(Segment(Point(2,-2), Point(2,-40)))
    simple_map.add_line(Segment(Point(2,-2), Point(40,-2)))
    simple_map.add_line(Segment(Point(40,-2), Point(40,-40)))
    sonar = sonar(50, 25, Point(50,50), simple_map)


    master = Tk()
    w = Canvas(master)
    w.pack()
    for i in [x * 5 for x in range(360/5)]:
        if i > 270:
            break
        pt = sonar.point_at_angle(135+i)
        w.create_oval(pt[0], pt[1], pt[0] + 2, pt[1] + 2)
    w.mainloop()
