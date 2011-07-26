#!usr/bin/python
from math import sqrt, cos, sin, radians
from shapely import *
from shapely.geometry import LineString, Point
from Tkinter import Tk, Canvas
import time

global canvas

class gui:

    def __init__(self, sonar):
        self.tk = Tk()
        self.canvas = Canvas(self.tk)
        self.canvas.pack()
        self.sonar = sonar
        self.tk.after(20,self.redraw)
        self.tk.mainloop()
        
    def redraw(self):
        print 'redraw'
        self.draw_sonar_data()
        self.draw_map()
        self.tk.after(1000, self.redraw)
        
    def draw_sonar_data(self):
        print 'data'
        for line in sonar.scan_lines:
            draw_line(self.canvas, line)

    def draw_map(self):
        print 'map'
        sonar.map.draw(self.canvas)
        
    
class sonar:

    def __init__(self, rng, step, start_loc, map_, move_points):
        print 'Sonar initialised.'
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.move_points = move_points # tuples containing a point location and angle of the sonar.
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through 

        # Where the first pulse is directed from. Sonar
        # initialised so that the first pulse travels from -125, where
        # up is 0.
        self.initial_angle = 145
        self.map = map_ # Map to use the sonar in
        self.start_loc = start_loc # Starting location of the sonar in the map
        self.loc = start_loc # Current location of the sonar in the map
        self.current_angle = self.initial_angle

    def reset(self):
        self.ranges = []
        self.scan_lines = []
        self.intersection_points = []
        self.current_angle = self.initial_angle
        
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

class map_:
    # For the purposes of the simulation, each increment of 1 in the
    # coordinate space represents 10cm. i.e. (20,5) is 2m from the
    # origin in the x direction and 50cm from the origin in the y
    # direction.

    def __init__(self):
        self.lines = []
    
    def __repr__(self):
        rep = ""
        for line in self.lines:
            rep += str(line) + "\n"
        return rep
        
    def add_line(self, line):
        self.lines.append(line)

    def draw(self, canvas):
        for line in self.lines:
            draw_line(canvas, line)

def draw_circle_from_centre(canvas, radius, centre):
    # probably the wrong way around, technically, but since it's a
    # circle it makes no difference really.
    tl = Point(centre.x - radius, centre.y + radius)
    br = Point(centre.x + radius, centre.y - radius)
    canvas.create_oval(tl.x, tl.y, br.x, br.y)

def draw_line(canvas, line):
    c = line.coords
    canvas.create_line(c[0][0], c[0][1], c[1][0], c[1][1])

def draw_point(canvas, point):
    pt = point
    canvas.create_oval(pt.x - 1, pt.y - 1, pt.x + 1, pt.y + 1)

if __name__ == '__main__':
    simple_map = map_()
    simple_map.add_line(LineString([(2,2),(2,40)]))
    simple_map.add_line(LineString([(2,2),(40,2)]))
    simple_map.add_line(LineString([(40,2),(40,40)]))
    simple_map.add_line(LineString([(2,40),(40,40)]))
                        
    sonar = sonar(50, 25, Point(20,20), simple_map, [])
    ab = gui(sonar)
