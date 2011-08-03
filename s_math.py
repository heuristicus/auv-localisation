#!/usr/bin/python
from math import sin, radians, cos, e, pi, sqrt
from shapely import *
from shapely.geometry import LineString, Point
import sys, random

class SonarMath:

    def get_intersect_point(self, location, scan_line, map_):
        x = []
        for line in map_.lines:
            x.append(scan_line.intersection(line))
            #print x
            
        min_dist = sys.maxint
        closest = None
        for c in x:
            cur_dist = c.distance(location)
            if cur_dist < min_dist:
                min_dist = cur_dist
                closest = c
        return closest
    
    def intersect_distance(self, location, intersect, minrange, maxrange):
        if not intersect:
            #print 'no intersection point to check distance to'
            return -1
        else:
            dist = intersect.distance(location)
            print 'distance is %d'%(dist)
            if minrange < dist < maxrange:
                return dist
            else:
                print 'Distance not within tolerated range.'
                return -1

    def get_scan_line(self, location, angle, length):
        pt = self.point_at_angle(location, angle, length)
        ln = LineString([location.coords[0], pt.coords[0]])
        return ln
       
    def point_at_angle(self, centre, degrees, radius):
        # (x', y') = (x + r cos a, y + r sin a)
        # x,y = centre point, r = radius, a = angle
        return Point(centre.x + (radius * cos(radians(degrees))), centre.y + (radius * sin(radians(degrees))))

    def apply_range_noise(self, lst, sigma):
        noise_ranges = []
        for i in lst:
            noise_ranges.append(random.gauss(i,sigma) if i is not -1 else -1)
        return noise_ranges

    def apply_point_noise(self, x, y, xsigma, ysigma):
        x = random.gauss(x, xsigma)
        y = random.gauss(y, ysigma)
        return (x,y)

    def get_noise(self, value, sigma):
        return random.gauss(value, sigma)

    def get_move_vector(self, p1, p2):
        return (p2.x - p1.x, p2.y - p1.y)

    def rotate_vector(self, point, vector, angle):
        sn = sin(radians(angle))
        cs = cos(radians(angle))
        x = vector[0]*cs - vector[1]*sn + point.x + point.y*sn - point.x*cs
        y = vector[0]*sn + vector[1]*cs + point.y - point.x*sn - point.y*cs
        return (x,y)

    def gaussian(self, mu, sigma, x):
        p1 = 1/(sqrt(2*pi*pow(sigma,2)))
        p2 = pow(e, ((-1*pow((x-mu),2)))/2.0*pow(sigma,2))
        return p1*p2

if __name__ == '__main__':
    a = SonarMath()
    #a.rotate_vector(Point(20,8), (40,80), -30)
    #print a.get_move_vector(Point(10,10), Point(5,5))
    #print a.gaussian(2,1,2)
