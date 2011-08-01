#!/usr/bin/python
from math import sin, radians, cos
from shapely import *
from shapely.geometry import LineString, Point
import sys

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
            #print 'distance is %d'%(dist)
            if minrange < dist < maxrange:
                return dist
            else:
                #print 'Distance not within tolerated range.'
                return -1

    def get_scan_line(self, location, angle, length):
        pt = self.point_at_angle(location, angle, length)
        ln = LineString([location.coords[0], pt.coords[0]])
        return ln
       
    def point_at_angle(self, centre, degrees, radius):
        # (x', y') = (x + r cos a, y + r sin a)
        # x,y = centre point, r = radius, a = angle
        return Point(centre.x + (radius * cos(radians(degrees))), centre.y + (radius * sin(radians(degrees))))
