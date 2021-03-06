#!/usr/bin/python
import random

class ParticleList:
    
    def __init__(self, particle_num):
        self.max_p = particle_num
        self.particles = []

    def add(self, particle):
        if len(particles) < self.max_p:
            self.particles.append(particle)
            return True
        else:
            return False
        
    def list(self):
        return self.particles
    
    def initialised(self):
        return True if self.particles else False

    def max_particles(self):
        return self.max_p

    def cur_particles(self):
        return len(self.particles)

    def best(self):
        """Find the particle with the highest weight"""
        m = 0
        best = None
        for p in self.particles:
            if p.wt > m:
                best = p
                m = p.wt
        return best

    def weights(self):
        """Get the weights for all particles in the list"""
        return [p.wt for p in self.particles]

    def locs(self):
        return [p.loc.coords[0] for p in self.particles]

    def angles(self):
        return [p.initial_angle for p in self.particles]

    def resample(self):
        """Resample the particles in the list probabilistically -
        particles with a higher weight have a higher probability of
        being chosen to be duplicated. Any particles not chosen are
        discarded."""
        if not self.particles or sum(self.weights()) is 0:
            return # Make sure this is only performed if you have the data required
        new_list = []
        wts = self.weights()
        s = sum(wts) # sum of the weights used to get the multiplier for the random value
        # get a number of random values equal to the number of particles, for which the range is 0 <= random <= sum of weights
        rands = [random.random() * s for i in range(len(self.particles))]
        self.wt_sum = []
        # get a list of values that correspond to the upper bounds for
        # a certain particle's weight.
        for i in range(len(wts)):
            if i is 0:
                self.wt_sum.append(wts[i])
            else:
                self.wt_sum.append(wts[i] + self.wt_sum[i-1])

        # For each of the random values, see which particle's weight
        # range it falls into
        n = map(self.wt_less, rands)
        # Create copies of the particles in the array locations from
        # the above calculation
        self.particles = [self.particles[i].copy() for i in n]
                        
    def wt_less(self, val):
        """Returns the list index of the range that the given value
        falls into."""
        for i in range(len(self.wt_sum)):
            if val < self.wt_sum[i]:
                return i
