#!/usr/bin/python
from shapely.geometry import Point

class MoveList:
    
    def __init__(self):
        self.movelist = []
        self.pointer = -1

    def __repr__(self):
        s = ''
        for point in self.movelist:
            s += str(point.coords[0])
        return s

    def read_from_file(self, filename):
        tmp = []
        ml = []
        tmp = open(filename, 'r').read().split(' ')
        tmp = map(int,tmp[:-1])
        for i in range(len(tmp)/2):
            ml.append(Point(tmp[i*2], tmp[i*2+1]))
        self.movelist =  ml

    def next(self):
        self.pointer += 1
        return self.current()

    def previous(self):
        self.pointer -= 1
        return self.current()

    def current(self):
        try:
            return self.movelist[self.pointer]
        except IndexError:
            print 'Either the start or end of the list has been reached.'
            return -1
            
    def get_list(self):
        return self.movelist
