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
        #self.math_pos = loc if loc[1] > 0 else Point(loc[0], loc[1] * -1) # mathematical representation of location (flipped y axis)
        self.math_pos = Point(loc[0], loc[1] * -1) # mathematical representation of location (flipped y axis)
        self.current_angle = self.initial_angle

    def get_ranges(self):
        angle_swept = 0
        while angle_swept < self.angle_range:
            #print 'new sonar ping'
            distance = self.point_distance(self.math_pos, self.get_intersect_point(self.get_scan_line()))
            self.ranges.append(distance)
            angle_swept += self.step
            self.current_angle += self.step
        print self.ranges

    def get_intersect_point(self, scan_line):
        # Return the first intersection point found on the line.  This
        # method will cause problems because if a line intersects with
        # two lines, and one is closer than the other, depending on
        # each line's position in the list (if the farther line comes
        # first in the list, the intersection with that line will be
        # returned, which is an error. Should be possible to fix by
        # appending intersection points to a list and then returning
        # the one whose distance from the sonar is smaller.
        for line in self.map.lines:
            print line, scan_line
            #print 'intersection check'
            i = intersection(scan_line, line)
            if i:
                self.intersection_points.append(i)
                return i

    def point_distance(self, sonar_loc, intersect):
        
        if intersect:
            print intersect
            dist = sqrt(pow(sonar_loc[0]-intersect[0][0], 2) + pow(sonar_loc[1]-intersect[0][1], 2))
            # Distance should not ever exceed max range, but check it anyway.
            # return the actual distance only if it is within a certain range.
            #print dist
            if self.min_range < dist < self.max_range:
                # multiply distance by 10 since each 1 represents 10cm
                return dist * 10
        
        # pretend that we can't resolve distances farther than the
        # sonar's range, and closer than a certain distance. Also
        # return -1 when there is no intersection
        return -1

    def get_scan_line(self):
        end_point = self.point_at_angle(self.current_angle)
        #print end_point
        line = Segment(self.math_pos, end_point)
        self.scan_lines.append(line)
        return line

    def point_at_angle(self, degrees):
        # (x', y') = (x + r cos a, y + r sin a)
        # x,y = centre point, r = radius, a = angle
        return Point(self.math_pos[0] + (self.max_range * cos(radians(degrees))), self.math_pos[1] + (self.max_range * sin(radians(degrees))))

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
    sonar = sonar(50, 25, Point(10,10), simple_map)
   
    master = Tk()
    w = Canvas(master)
    w.pack()
    w.create_line(2,2,2,40)
    w.create_line(2,2,40,2)
    w.create_line(40,2,40,40)
    for i in range(360):
        pt = sonar.point_at_angle(i)
        w.create_oval(pt[0], pt[1], pt[0]+2, pt[1] + 2)
    #w.bind("<Button-1>", sonar.get_ranges)
    #w.mainloop()

    #print sonar.point_distance(Point(5,10), Point(20,40))
    sonar.get_ranges()
    for line in sonar.scan_lines:
        w.create_line(line[0][0], line[0][1], line[1][0], line[1][1])
    for point in sonar.intersection_points:
        w.create_oval(point[0][0], point[0][1], point[0][0] + 2, point[0][1] + 2)
    w.mainloop()
    
    
