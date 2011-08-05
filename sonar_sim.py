#!usr/bin/python
from math import sqrt, cos, sin, radians, acos, degrees, asin, atan2
from Tkinter import Tk, Canvas
from shapely import *
from shapely.geometry import Point
import random, map_rep, gui, sys, move_list, s_math, particle, particle_list

global canvas

class sonar:

    def __init__(self, map_, move_list, rng=50, step=25, particle_number=5, ):
        print 'Sonar initialised.'
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.particles = particle_list.ParticleList()
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
        self.num_particles = particle_number
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
        """Moves the simulation into the next step."""
        next = self.move_list.next()
        current = self.loc
        if next is -1:
            return -1 # no more steps in list
        else:
            self.generate_particles(self.num_particles) # only if not already done
            self.particles.resample() # only if particles exist and have weights
            self.move_to(next[0], next[1]) # move sonar to its next position
            self.get_ranges() # get sonar ranges
            self.math.apply_range_noise(self.ranges, 0.5) # apply noise to the sonar ranges 
            # get the vector required to move from the sonar's current
            # point to the next point
            move_vector = self.math.get_move_vector(current, next[0]) 
            for particle in self.particles.list():
                # move each particle along the vector, and set its
                # scan start angle tothe sonar's. This method
                # introduces noise into both of those measurements.
                particle.move(move_vector, self.initial_angle)
                # get the ranges that the sonar would see if it were
                # in the same position and orientation as the sonar
                particle.get_ranges()
                # weight each particle based on the variation of its
                # range measurements with the measurements received
                # from the sonar.
                self.weight_particle(particle)
            return 1 # steps remain in list

    def weight_particle(self, particle):
        """Weights the given particle according to the difference
        between its ranges tand the ranges detected by the sonar."""
        prob_sum = 0
        for i in range(len(particle.ranges)):
            # Sonar returns -1 if the range received is not in the
            # tolerated range. In this case, the measurement is not
            # reliable, so only give a small weight increase.
            if self.ranges[i] is -1 and particle.ranges[i] is -1:
                prob_sum += 0.03
            else:
                # Calculate the probability of the particle range
                # measurement given that the sonar range measurement
                # might have a certain amount of noise
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
        """Moves the sonar to a random position within a height x
        width rectangle."""
        self.move_to(Point(random.randint(0, width), random.randint(0, height)), random.randint(0,360))

    def move_to_random_bounded(self, height, width, bound):
        """Moves to a random location within a height x width
        rectangle, but within a bounded range of its current
        location"""
        self.move_to(Point(random.randint(self.loc.x - bound, self.loc.x + bound), random.randint(self.loc.y - bound, self.loc.y + bound)), random.randint(self.initial_angle - bound, self.initial_angle - bound))
        
    def get_ranges(self):
        """Get the ranges that the sonar would receive at its current
        map position if its sensors were perfect."""
        self.reset() # reset arrays containing scan lines, ranges etc. 
        for i in range(360/self.step): # loop over the total number of measurements to take
            if self.current_angle > self.initial_angle + self.angle_range:
                # The whole scan has been completed, just a second check.
                break
            # get the line from the sonar to the point of max range
            ln = self.math.get_scan_line(self.loc, self.current_angle, self.max_range)
            # get the intersection point with the scan line on the map
            # that is closest to the current sonar location
            intersect = self.math.get_intersect_point(self.loc, ln, self.map)
            # calculate the distance to the intersection point, with
            # some parameters which limit the data to a certain range
            dist = self.math.intersect_distance(self.loc, intersect, self.min_range, self.max_range,)
            self.ranges.append(dist) # store the calculated distance
            # Store the other objects for drawing later if necessary
            self.scan_lines.append(ln)
            self.intersection_points.append(intersect)
            self.current_angle += self.step # increment the angle to the angle of the next measurement
        
    def generate_particles(self, number):
        """Create a number of particles."""
        if not self.particles.list():
            for i in range(number):
                # Create a particle within a gaussian range of the current sonar location
                self.particles.add(particle.Particle(Point(self.math.apply_point_noise(self.loc.x, self.loc.y, 10, 10)), self))
                
if __name__ == '__main__':
    simple_map = map_rep.map_(sys.argv[1])
    mvlist = move_list.MoveList()
    mvlist.read_from_file(sys.argv[2])
    #mvlist = move_list.MoveList([Point(0,0)])
    param = [simple_map, mvlist, 50, 15, 5]
    sonar = sonar(*param)
    #sonar = sonar(simple_map, mvlist, rng=50, step=15, particle_number=5)
    #a = particle.Particle(sonar.loc, sonar)
    #a.get_ranges()
    ab = gui.gui(sonar)
