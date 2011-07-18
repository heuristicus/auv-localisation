#!/bin/python

class particle:

    def __init__(self):
        self.loc = (0,0)
        self.wt = 0
        

class sonar:

    def __init__(self, rng, step, loc, map_):
        self.distances = [] # Distances to objects in the map on previous pulse
        self.range = rng # Range of the sonar pulse
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through
        self.initial_angle = 225 # Where the first pulse is directed from
        self.map = map_ # Map to use the sonar in
        self.loc = loc # The starting position of the sonar in the map

    def get_ranges(self):
        angle_swept = 0
        while angle_swept != angle_range:
            

            angle_swept += self.step

class map:
    
    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)
        
if __name__ == '__main__':
    print 'not implemented yet.'
