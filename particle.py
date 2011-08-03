#!/usr/bin/python
import s_math
from shapely.geometry import Point

class Particle:
    
    def __init__(self, loc, sonar, wt=0):
        self.loc = loc
        self.wt = wt
        self.scan = []
        self.int = []
        self.map = sonar.map
        self.maxrange = sonar.max_range
        self.minrange = sonar.min_range
        self.initial_angle = sonar.initial_angle
        self.current_angle = self.initial_angle
        self.angle_range = sonar.angle_range
        self.step = sonar.step
        self.math = s_math.SonarMath()

    def get_ranges(self):
        self.scan = []
        self.int = []
        self.current_angle = self.initial_angle
        self.ranges = []
        # loop might not work for certain step numbers?
        #for i in [x * self.step for x in map(lambda x:x+1, range(360/self.step))]:
        #print self.step, self.initial_angle, self.current_angle
        for i in range(360/self.step):
            if self.current_angle > self.initial_angle + self.angle_range:
                break
            ln = self.math.get_scan_line(self.loc, self.current_angle, self.maxrange)
            intersect = self.math.get_intersect_point(self.loc, ln, self.map)
            dist = self.math.intersect_distance(self.loc, intersect, self.minrange, self.maxrange,)
            self.scan.append(ln)
            self.int.append(intersect)
            self.ranges.append(dist)
            self.current_angle += self.step

    def move(self, vector, angle):
        angle_noise = self.math.get_noise(0, 5)
        vec = self.math.rotate_vector(self.loc, vector, angle_noise)
        endpt = Point(vec[0] + self.loc.x, vec[1] + self.loc.y)
        n_end = Point(self.math.apply_point_noise(endpt.x, endpt.y, 0.5, 0.5))
        self.initial_angle = angle + angle_noise
        self.loc = n_end
