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
        particles.append(Particle(random.gauss(loc[0], 40), random.gauss(loc[1], 40), 0))

    print particles

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
