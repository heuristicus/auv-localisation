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
        try:
            self.pointer += 1
        except IndexError:
            print 'End of movelist reached.'
            return -1
        return self.current()

    def previous(self):
        try:
            self.pointer -= 1
        except IndexError:
            print 'At start of movelist.'
            return -1
        return self.current()

    def current(self):
        return self.movelist[self.pointer]

    def get_list(self):
        return self.movelist
