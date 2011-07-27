#!usr/bin/python
from math import sqrt, cos, sin, radians, acos, degrees, asin, atan2
from shapely import *
from shapely.geometry import LineString, Point
from Tkinter import Tk, Canvas
import random, map_rep, gui, sys, move_list

global canvas

class sonar:

    def __init__(self, rng, step, map_, move_list):
        print 'Sonar initialised.'
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.move_list = move_list # tuples containing a point location and angle of the sonar.
        self.current_point = -1 # starts at a negative index, first point provided by map
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through 

        # Where the first pulse is directed from. Sonar initialised so
        # that the first pulse travels from -125, where up is 0.
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
        print next
        if next is -1:
            return -1
        else:
            self.move_to(next, self.initial_angle) # MODIFY THE SECOND PARAMETER
            self.get_ranges()
            return 1
        
    def move_to(self, loc, rotation):
        """Moves the sonar to a specified location with the specified
        rotation applied. The rotation is assumed to be a new setting
        and not an increment on the current rotation."""
        self.loc = loc
        self.initial_angle = rotation

    def move_to_random(self, height, width):
        self.move_to(Point(random.randint(0, width), random.randint(0, height)), random.randint(0,360))

    def move_to_random_bounded(self, height, width, bound):
        self.move_to(Point(random.randint(self.loc.x - bound, self.loc.x + bound), random.randint(self.loc.y - bound, self.loc.y + bound)), random.randint(self.initial_angle - bound, self.initial_angle - bound))
        
    def get_ranges(self):
        #print 'Getting ranges'
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
        #print 'Finished getting ranges.'

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
        
    def angle_at_pt(self, point, centre):
        """Calculates the angle of a point on a circle"""
        radius = point.distance(centre)
        c = degrees(acos((centre.x - point.x) / radius))
        s = degrees(asin((centre.y - point.y) / radius))

        print c, s
        
        # Such a terrible way of doing this.
        if 90 <= c <= 180 and -90 <= s <= 0:
            return -s
            #print 'sector 1'
        elif 0 <= c <= 90 and -90 <= s <= 0:
            return 180 + s
            #print 'sector 2'
        elif 0 <= c <= 90 and 0 <= s <= 90:
            return 180 + s
            #print 'sector 3'
        elif 90 <= c <= 180 and 0 <= s <= 90:
            return 360 - s
            #print 'sector 4'
                
if __name__ == '__main__':
    simple_map = map_rep.map_(sys.argv[1])
    #mvlist = move_list.MoveList()
    #mvlist.read_from_file(sys.argv[2])
    mvlist = move_list.MoveList([Point(0,0)])
    sonar = sonar(50, 25, simple_map, mvlist)
    sonar.move_to(Point(0,0), 0)
    sonar.angle_at_pt(Point(40,60), Point(40,40))
    sonar.angle_at_pt(Point(60,40), Point(40,40))
    sonar.angle_at_pt(Point(40,20), Point(40,40))
    sonar.angle_at_pt(Point(20,40), Point(40,40))
    print '--'
    for i in range(360):
        print '--'
        #sonar.point_at_angle(i)
        sonar.angle_at_pt(sonar.point_at_angle(i), sonar.loc)
    #ab = gui.gui(sonar)
