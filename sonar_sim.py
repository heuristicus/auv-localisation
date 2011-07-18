#!/bin/python
from sympy import intersection
from sympy.geometry import Line, Point
from math import sqrt, cos, sin, radians

class particle:

    def __init__(self):
        self.loc = (0,0)
        self.wt = 0
        

class sonar:

    def __init__(self, rng, step, loc, map_):
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through
        self.initial_angle = 225 # Where the first pulse is directed from
        self.map = map_ # Map to use the sonar in
        self.loc = loc # The starting position of the sonar in the map
        self.current_angle = self.initial_angle

    def get_ranges(self):
        angle_swept = 0
        while angle_swept < self.angle_range:
            scan_line = self.get_scan_line()
            print scan_line
            intersect_point = self.get_intersect_point(scan_line)
            distance = self.point_distance(self.loc, intersect_point)
            self.ranges.append(distance)
            angle_swept += self.step
            self.current_angle += self.step

    def get_intersect_point(self, scan_line):
        # Return the first intersection point found on the line
        for line in self.map.lines:
            i = intersection(scan_line, line)
            print i
            if i:
                return i

    def point_distance(self, p1, p2):
        # multiply distance by 10 since each 1 represents 10cm
        dist = 10 * sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1]-p2[1], 2))
        if self.min_range < dist < self.max_range:
            # pretend that we can't resolve distances farther than the
            # sonar's range, and closer than a certain distance.
            return -1
        else:
            return dist

    def get_scan_line(self):
        end_point = self.point_at_angle(self.current_angle)
        print end_point
        return Line(self.loc, end_point)

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
    simple_map.add_line(Line(Point(2,2), Point(2,40)))
    simple_map.add_line(Line(Point(2,2), Point(40,2)))
    simple_map.add_line(Line(Point(40,2), Point(40,40)))
    sonar = sonar(50, 5, Point(20,20), simple_map)
    #print sonar.point_distance(Point(5,10), Point(20,40))
    sonar.get_ranges()
    
