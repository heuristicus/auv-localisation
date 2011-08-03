#!/usr/bin/python
from shapely.geometry import Point
import sys

class MoveList:
    
    def __init__(self, movelist=[]):
        self.movelist = movelist
        self.pointer = -1

    def __repr__(self):
        s = ''
        for point in self.movelist:
            s += 'Point: %s \nRotation: %s\n'%(str(point[0].coords[0]), str(point[1]))
        return s[:-2] # crude way to get rid of last newline

    def read_from_file(self, filename):
        tmp = []
        ml = []
        tmp = open(filename, 'r').read().split(' ')
        tmp = map(float,tmp[:-1])
        for i in range(len(tmp)/3):
            ml.append([Point(tmp[i*3], tmp[i*3+1]), tmp[i*3+2]])
        self.movelist =  ml

    def next(self):
        self.pointer += 1
        return self.current()

    def previous(self):
        self.pointer -= 1
        return self.current()
    
    def get_previous(self):
        return self.movelist[self.pointer - 1]
    
    def first(self):
        return self.movelist[0]

    def current(self):
        try:
            if self.pointer < 0:
                raise IndexError
            return self.movelist[self.pointer]
        except IndexError:
            print 'Either the start or end of the list has been reached.'
            return -1
            
    def get_list(self):
        return self.movelist

if __name__ == '__main__':
    m = MoveList()
    m.read_from_file(sys.argv[1])
    print m
