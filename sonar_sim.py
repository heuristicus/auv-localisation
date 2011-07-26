#!usr/bin/python
from math import sqrt, cos, sin, radians
from shapely import *
from shapely.geometry import LineString, Point
from Tkinter import *
import time

global canvas

class sonar:

    def __init__(self, rng, step, loc, map_):
        self.ranges = [] # Distances to objects in the map on previous pulse
        self.scan_lines = []
        self.intersection_points = []
        self.max_range = rng # Maximum range of the sonar pulse in cm
        self.min_range = 4
        self.step = step # Angle moved by the sonar head between each pulse
        self.angle_range = 270 # Total angle that the sonar sweeps through 

        # Where the first pulse is directed from. Sonar
        # initialised so that the first pulse travels from -125, where
        # up is 0.
        self.initial_angle = 145
        self.map = map_ # Map to use the sonar in
        self.loc = loc # The position of the sonar in the map in computer coords
        self.current_angle = self.initial_angle

    def reset(self):
        self.ranges = []
        self.scan_lines = []
        self.intersection_points = []
        self.current_angle = self.initial_angle
        
    def get_ranges(self):
        self.reset()
        for i in [x * self.step for x in map(lambda x:x+1, range(360/self.step))]:
            #print 'new scan'
            if self.current_angle > self.initial_angle + self.angle_range:
                break
            ln = self.get_scan_line()
            intersect = self.get_intersect_point(ln)
            dist = self.point_distance(intersect)
            self.ranges.append(dist)
            self.current_angle += self.step

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

    def point_distance(self, intersect):
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

def angle_point_test(start, step):
    create_canvas()
    start_angle = start
    pt = sonar.point_at_angle(start_angle)
    canvas.create_oval(pt[0], pt[1], pt[0] + 2, pt[1] + 2, fill='red')
    for i in [x * step for x in map(lambda x:x+1, range(360/step))]:
        if i > 265:
            break
        pt = sonar.point_at_angle(start_angle+i)
        draw_point(canvas, pt)
    canvas.mainloop()

def scan_line_test():
    sonar.get_ranges()
    create_canvas()
    for line in sonar.scan_lines:
        draw_line(canvas, line)
    canvas.mainloop()

def intersection_point_test():
    sonar.get_ranges()
    create_canvas()
    for line in sonar.scan_lines:
        draw_line(canvas,line)
    for pt in sonar.intersection_points:
        draw_point(canvas,pt)
    simple_map.draw(canvas)
    canvas.mainloop()

def create_canvas():
    global canvas
    master = Tk()
    canvas = Canvas(master)
    canvas.pack()

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
                        
    sonar = sonar(50, 25, Point(20,20), simple_map)
    #sonar.point_at_angle(50)
    #create_canvas()
    #draw_circle_from_centre(canvas, 50, Point(10,30))
    intersection_point_test()
    #print sonar.intersection_pts
    #print sonar.scan_lines
    #print sonar.ranges
    #scan_line_test()
    #angle_pt_test(0,10)
