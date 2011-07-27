#!usr/bin/python
from math import sqrt, cos, sin, radians
from shapely import *
from shapely.geometry import LineString, Point
from Tkinter import Tk, Canvas
import random, map_rep, gui, sys

global canvas

class sonar:

    def __init__(self, rng, step, map_, move_points):
        print 'Sonar initialised.'
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.move_points = move_points # tuples containing a point location and angle of the sonar.
        self.current_point = -1 # starts at a negative index, first point provided by map
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through 

        # Where the first pulse is directed from. Sonar
        # initialised so that the first pulse travels from -125, where
        # up is 0.
        self.initial_angle = 145
        self.map = map_ # Map to use the sonar in
        p = map_.get_sonar_pos()
        self.start_loc = Point(p[0], p[1]) # Starting location of the sonar in the map
        self.loc = self.start_loc # Current location of the sonar in the map
        self.current_angle = self.initial_angle

    def reset(self):
        self.ranges = []
        self.scan_lines = []
        self.intersection_points = []
        self.current_angle = self.initial_angle

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

    def next_point(self):
        try:
            self.current_point += 1
        except IndexError:
            print 'Reached the end of the move sequence.'
        pt = self.move_points[self.current_point]
        move_to(pt[0], pt[1])
  
    def move_to(self, loc, rotation):
        """Moves the sonar to a specified location with the specified
        rotation applied. The rotation is assumed to be a new setting
        and not an increment on the current rotation."""
        self.loc = loc
        self.initial_angle = rotation

    def move_to_random(self, height, width):
        self.move_to(Point(random.randint(0, width), random.randint(0, height)), random.randint(0,360))

    def move_to_random_bounded(self, height, width, bound):
        self.move_to(Point(random.randint(self.loc.x - bound, self.loc.x + bound), random.randint(self.loc.y - bound, self.loc.y + bound)), random.randint(self.initial_angle - bound), self.initial_angle - bound)
        
    def get_ranges(self):
        print 'Getting ranges'
        self.reset()
        for i in [x * self.step for x in map(lambda x:x+1, range(360/self.step))]:
            #print 'new scan'
            if self.current_angle > self.initial_angle + self.angle_range:
                break
            ln = self.get_scan_line()
            intersect = self.get_intersect_point(ln)
            dist = self.intersect_distance(intersect)
            self.ranges.append(dist)
            self.current_angle += self.step
        print 'Finished getting ranges.'

    def get_intersect_point(self, scan_line):
        # This will need to be fixed to make sure that only the point
        # closest to the sonar is returned when the same scan line
        # intersects two different map lines.
        for line in self.map.lines:
            x = scan_line.intersection(line)
            #print x
            if x:
                self.intersection_points.append(x)
                return x

        #print 'No intersection'
        self.intersection_points.append(None)
        return None

    def intersect_distance(self, intersect):
        if not intersect:
            #print 'no intersection point to check distance to'
            return -1
        else:
            dist = intersect.distance(self.loc)
            #print 'distance is %d'%(dist)
            if self.min_range < dist < self.max_range:
                return dist
            else:
                #print 'Distance not within tolerated range.'
                return -1

    def get_scan_line(self):
        pt = self.point_at_angle(self.current_angle)
        ln = LineString([self.loc.coords[0], pt.coords[0]])
        self.scan_lines.append(ln)
        return ln
       
    def point_at_angle(self, degrees):
        # (x', y') = (x + r cos a, y + r sin a)
        # x,y = centre point, r = radius, a = angle
        return Point(self.loc.x + (self.max_range * cos(radians(degrees))), self.loc.y + (self.max_range * sin(radians(degrees))))

if __name__ == '__main__':
    #simple_map = map_()
    #simple_map.add_line(LineString([(2,2),(2,40)]))
    #simple_map.add_line(LineString([(2,2),(40,2)]))
    #simple_map.add_line(LineString([(40,2),(40,40)]))
    #simple_map.add_line(LineString([(2,40),(40,40)]))
    simple_map = map_rep.map_(sys.argv[1])
    sonar = sonar(50, 25, simple_map, [])
    ab = gui.gui(sonar)
