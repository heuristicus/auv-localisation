#!/usr/bin/python
import sys
from shapely.geometry import LineString

class map_:
    # For the purposes of the simulation, each increment of 1 in the
    # coordinate space represents 10cm. i.e. (20,5) is 2m from the
    # origin in the x direction and 50cm from the origin in the y
    # direction.

    def __init__(self, fname=''):
        self.lines = []
        if fname:
            self.load_map_from_file(fname)
    
    def __repr__(self):
        rep = ""
        for line in self.lines:
            rep += str(line) + "\n"
        return rep
        
    def add_line(self, line):
        self.lines.append(line)

    def draw(self, canvas):
        for line in self.lines:
            draw_line(canvas, line)

    def get_sonar_pos(self):
        return self.sonar_pos

    def load_map_from_file(self, filename):
        f = open(filename, 'r')
        s = f.read()
        vals = map(int, s.split(' ')[:-1])
        # Maybe move the sonar position from being defined on the map
        # to being defined in the sequence of points to move along?
        pt = vals
        for i in map(lambda x:x*4, range(len(pt)/4)):
            self.add_line(LineString([(pt[i], pt[i+1]),(pt[i+2], pt[i+3])]))

if __name__ == '__main__':
    m = map_()
    m.load_map_from_file(sys.argv[1])
