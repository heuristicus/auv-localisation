#!/bin/python
from sympy.geometry import Line, Point

class particle:

    def __init__(self):
        self.loc = (0,0)
        self.wt = 0
        

class sonar:

    def __init__(self, rng, step, loc, map_):
        self.distances = [] # Distances to objects in the map on previous pulse
        self.range = rng # Range of the sonar pulse in cm
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through
        self.initial_angle = 225 # Where the first pulse is directed from
        self.map = map_ # Map to use the sonar in
        self.loc = loc # The starting position of the sonar in the map
        self.current_angle = self.initial_angle

    def get_ranges(self):
        angle_swept = 0
        while angle_swept < angle_range:
            
            angle_swept += self.step

    def point_at_angle(self, degrees):
        # (x', y') = (x + r cos a, y + r sin a)
        # x,y = centre point, r = radius, a = angle
        return Point(self.loc[0] + (self.rng * math.cos(degrees), self.loc[1] + (self.rng * math.cos(degrees))

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
    print 'not implemented yet.'
    simple_map = map_()
    simple_map.add_line(Line(Point(2,2), Point(2,40)))
    simple_map.add_line(Line(Point(2,2), Point(40,2)))
    simple_map.add_line(Line(Point(40,2), Point(40,40)))
    sonar = sonar()
                                    
           
    
