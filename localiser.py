#!/bin/python
import map_rep, gui, sys, move_list, s_math, particle, particle_list

class Localiser:

    def __init__(self, particle_num, mapfile, sonar, paramfile=''):
        self.particles = particle_list.ParticleList(particle_num)
        self.map = map_rep.MapRep(fname=mapfile)
        self.read_params(fname=paramfile)
        self.sonar = ''

    def generate_particles(self):
        """Create a number of particles."""
        sonar_loc = self.sonar.loc()
        # the sonar only knows where it is in the first step (let's
        # pretend), and so when you don't know where the sonar is we
        # generate points based on our localised value
        if not sonarloc: 
            sonarloc = self.estimated_loc
        if not self.particles.initialised():
            for i in range(self.particles.max_particles()):
                # Create a particle within a gaussian range of the current sonar location
                self.particles.add(particle.Particle(Point(self.math.apply_point_noise(self.sonar.x, self.sonar.y, self.loc_noise, self.loc_noise)), self))

    def weight_particle(self, particle):
        """Weights the given particle according to the difference
        between its ranges tand the ranges detected by the sonar."""
        prob_sum = 0
        if len(self.ranges) is not len(particle.ranges):
            print 'ERROR - sonar and particles do not have the same number of ranges'
            print self.ranges, len(self.ranges)
            print '\n'
            print particle.ranges, len(particle.ranges)
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
                prob_sum += self.math.gaussian(self.ranges[i], self.rng_noise, particle.ranges[i])
        particle.wt = prob_sum
        return prob_sum

    def sim_step(self):
        """Moves the simulation into the next step."""
        next = self.move_list.next()
        current = self.loc if self.first else self.move_list.get_previous()[0] # THIS IS PROBABLY NOT THE ACTUAL LOCATION OF THE SONAR - noise has been added!
        if next is -1:
            return -1 # no more steps in list
        else:
            self.generate_particles(self.num_particles) # only if not already done
            self.particles.resample() # only if particles exist and have weights
            move_vector = self.math.get_move_vector(current, next[0])
            self.move_to_noisy(move_vector, next[1]) # move sonar to its next position
            self.get_ranges() # get sonar ranges
            self.math.apply_range_noise(self.ranges, self.rng_noise) # apply noise to the sonar ranges 
            # get the vector required to move from the sonar's current
            # point to the next point
             
            for particle in self.particles.list():
                # move each particle along the vector, and set its
                # scan start angle tothe sonar's. This method
                # introduces noise into both of those measurements.
                particle.move(move_vector, self.initial_angle)
                # get the ranges that the sonar would see if it were
                # in the same position and orientation as the sonar
                particle.get_ranges(self.scale)
                # weight each particle based on the variation of its
                # range measurements with the measurements received
                # from the sonar.
                self.weight_particle(particle)
            print self.get_localisation_error()
            self.save_info()
            return 1 # steps remain in list

    def get_localisation_error(self):
        lsa = self.particles.best().loc
        return (self.loc.x - lsa.x, self.loc.y - lsa.y)

    def read_params(self, fname):
        """Reads parameters from a file and saves them in a dictionary"""
        if not fname:
            self.ang_noise = 5
            self.loc_noise = 0.5
            self.rng_noise = 0.5
        else:
            f = open(fname)
            s = f.read().split('\n')[:-1]
            params = {}
            for param in s:
                z = param.split(' = ')
                params[z[0]] = float(z[1])
            self.ang_noise = params.get('ang_ns')
            self.loc_noise = params.get('loc_ns')
            self.rng_noise = params.get('rng_ns')

if __name__ == '__main__':
    l = Localiser()
