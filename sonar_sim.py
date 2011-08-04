#!usr/bin/python
from math import sqrt, cos, sin, radians, acos, degrees, asin, atan2
from Tkinter import Tk, Canvas
from shapely import *
from shapely.geometry import Point
import random, map_rep, gui, sys, move_list, s_math, particle, particle_list

global canvas

class sonar:

    def __init__(self, rng, step, map_, move_list):
        print 'Sonar initialised.'
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.particles =particle_list.ParticleList()
        self.move_list = move_list # tuples containing a point location and angle of the sonar.
        self.current_point = -1 # starts at a negative index, first point provided by map
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through 

        # Where the first pulse is directed from. Sonar initialised so
        # that the first pulse travels from -125, where up is 0.
        self.map = map_ # Map to use the sonar in
        start_point = move_list.first()
        self.start_loc = start_point[0] # Starting location of the sonar in the map
        self.loc = self.start_loc # Current location of the sonar in the map
        self.initial_angle = start_point[1]
        self.current_angle = self.initial_angle
        self.math = s_math.SonarMath()

    def reset(self):
        self.ranges = []
        self.scan_lines = []
        self.intersection_points = []
        self.current_angle = self.initial_angle

    def get_move_list(self):
        return self.move_list.get_list()

    def move_in_list(self, val, step='inc'):
        """Moves around in the movement sequence.  step can be either
        'inc' or 'jump'. inc will increment the current position by
        the value provided (i.e negatives work), and jump will jump to
        a position.
        """
        try:
            if step is 'inc':
                self.current_point += val
            if step is 'jump':
                self.current_point = val
        except IndexError:
            print 'Cannot %s to value %d. Length of list is %d, current pointer is %s'%('increment' if step is 'inc' else 'jump', val,  len(self.move_points), self.current_point)

    def sim_step(self):
        next = self.move_list.next()
        current = self.loc
        if next is -1:
            return -1 # no more steps in list
        else:
            if not self.particles.list():
                self.first = True
                self.generate_particles(10)
            self.move_to(next[0], next[1])
            self.get_ranges()
            self.math.apply_range_noise(self.ranges, 0.5)
            move_vector = self.math.get_move_vector(current, next[0])
            self.move_particles(move_vector)
            self.resample()
            self.first = False
            return 1 # steps remain in list

    def move_particles(self, vector):
        p_cp = []
        for particle in self.particles.list():
            if not self.first:
                particle.move(vector, self.initial_angle)
            particle.get_ranges()
            # print zip(self.ranges, particle.ranges)
            p_cp.append(self.compare_ranges(particle))
            # print '---------------------'
        print p_cp

    def resample(self):
        print 'a'

    def compare_ranges(self, particle):
        prob_sum = 0
        for i in range(len(particle.ranges)):
            if self.ranges[i] is -1 and particle.ranges[i] is -1:
                prob_sum += 0.03
            else:
                prob_sum += self.math.gaussian(self.ranges[i], 0.5, particle.ranges[i])
        particle.wt = prob_sum
        return prob_sum
                        
    def move_to(self, loc, rotation):
        """Moves the sonar to a specified location with the specified
        rotation applied. The rotation is assumed to be a new setting
        and not an increment on the current rotation."""
        self.loc = loc
        self.initial_angle = 315 - rotation #just a guess, works ok

    def move_to_random(self, height, width):
        self.move_to(Point(random.randint(0, width), random.randint(0, height)), random.randint(0,360))

    def move_to_random_bounded(self, height, width, bound):
        self.move_to(Point(random.randint(self.loc.x - bound, self.loc.x + bound), random.randint(self.loc.y - bound, self.loc.y + bound)), random.randint(self.initial_angle - bound, self.initial_angle - bound))
        
    def get_ranges(self):
        self.reset()
        # loop might not work for certain step numbers?
        #for i in [x * self.step for x in map(lambda x:x+1, range(360/self.step))]:
        for i in range(360/self.step):
            if self.current_angle > self.initial_angle + self.angle_range:
                break
            ln = self.math.get_scan_line(self.loc, self.current_angle, self.max_range)
            intersect = self.math.get_intersect_point(self.loc, ln, self.map)
            dist = self.math.intersect_distance(self.loc, intersect, self.min_range, self.max_range,)
            self.ranges.append(dist)
            self.scan_lines.append(ln)
            self.intersection_points.append(intersect)
            self.current_angle += self.step
        
    def generate_particles(self, number):
        for i in range(number):
            self.particles.add(particle.Particle(Point(self.math.apply_point_noise(self.loc.x, self.loc.y, 10, 10)), self))
                
if __name__ == '__main__':
    simple_map = map_rep.map_(sys.argv[1])
    mvlist = move_list.MoveList()
    mvlist.read_from_file(sys.argv[2])
    #mvlist = move_list.MoveList([Point(0,0)])
    sonar = sonar(50, 15, simple_map, mvlist)
    #a = particle.Particle(sonar.loc, sonar)
    #a.get_ranges()
    ab = gui.gui(sonar)
