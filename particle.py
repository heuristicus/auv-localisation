#!/usr/bin/python
import s_math

class Particle:
    
    def __init__(self, loc, sonar, wt=0):
        self.loc = loc
        self.wt = wt
        self.map = sonar.map
        self.maxrange = sonar.max_range
        self.minrange = sonar.min_range
        self.initial_angle = sonar.initial_angle
        self.current_angle = self.initial_angle
        self.angle_range = sonar.angle_range
        self.step = sonar.step
        self.math = s_math.SonarMath()

    def get_ranges(self):
        self.ranges = []
        # loop might not work for certain step numbers?
        #for i in [x * self.step for x in map(lambda x:x+1, range(360/self.step))]:
        for i in range(360/self.step):
            if self.current_angle > self.initial_angle + self.angle_range:
                break
            ln = self.math.get_scan_line(self.loc, self.current_angle, self.maxrange)
            intersect = self.math.get_intersect_point(self.loc, ln, self.map)
            dist = self.math.intersect_distance(self.loc, intersect, self.minrange, self.maxrange,)
            self.ranges.append(dist)
            self.current_angle += self.step

    def move(self, vector):
        n_vec = self.math.apply_point_noise(vector[0], vector[1])
