#!/usr/bin/python
import random
from Tkinter import *

global particles

def distribute(number, loc):
    """"Distribute a certain number of particles around a location in
    cartesian coordinates"""
    global particles
    particles = []
    for i in range(number):
        make_particle(loc, 40)

    print particles

def make_particle(loc, var):
    xval = random.gauss(loc[0], var)
    yval = random.gauss(loc[1], var)

    if xval > 0 and yval > 0:
        return Particle(xval, yval, gen_wt())


def gen_wt():
    # not sure what to do here yet - maybe proportional to the
    # proximity to the location?
    return 0

class Particle:
    
    def __init__(self, x, y, wt):
        self.x = x
        self.y = y
        self.wt = wt # weight

    def __repr__(self):
        return "(%d, %d)"%(self.x,self.y)

if __name__ == '__main__':
    distribute(300, [50,50])
    m = Tk()
    c = Canvas(m)
    c.pack()
    for particle in particles:
        c.create_oval(particle.x, particle.y, particle.x+2, particle.y +2)
    c.mainloop()
