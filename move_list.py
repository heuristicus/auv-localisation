#!/usr/bin/python

class MoveList:
    
    def __init__(self):
        self.movelist = []
        self.pointer = -1

    def read_from_file(self, filename):
        tmp = open(filename, 'r').read().split(' ')
        movelist = map(int, movelist[:-1])
        ptlist = []
        for i in range(len(movelist)/2):
            ptlist.append(Point(movelist[i*2], movelist[i*2+1]))
        print ptlist

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
