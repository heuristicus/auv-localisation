#!/usr/bin/python
import sys
import re

class TestParser():
    
    def __init__(self):
        self.make_lists()
        self.produce_output()

    def make_lists(self):
        f = open(sys.argv[1])
        data = f.read()
        
        # split each test to a separate list, ignoring the blank
        confs = data.split('newconf\n')[1:] 
        tests = []
        for conf in confs:
            # each test has a number of positions that the sonar goes
            # through according to the movelist, so split those up
            tests.append(re.split('\nnewtest', conf))
            splitsteps = []
        for test in tests:
            for num in map(lambda x: x + 1, range(len(test[1:]))):
                test[num] = re.split('step \d+\n', test[num])
                for step in range(len(test[num])):
                    test[num][step] = test[num][step].split('\n')
        
        confs = []
        starts = []
        ends = []
        steps = []
        for test in tests:
            confs.append(test[0])
            t_end = []
            t_start = []
            t_step = []
            for item in test[1:]:
                end = item[-1]
                t_end.append(end[0].split(' ')[1])
                start = item[0][1].split(' ')[1]
                t_start.append(start)
                step = item[1:-1]
                t_step.append(step)
            steps.append(t_step)
            ends.append(t_end)
            starts.append(t_start)
        self.confs = confs
        self.starts = starts
        self.steps = steps
        self.ends = ends
        for step in self.steps:
            for p in step:
                for r in p:
                    print r
                    print '\n'

    def produce_output(self):
        res = ''
        for i in range(len(self.confs)):
            for j in range(len(self.starts[i])):
                res += '%s\n'%(self.confs[i])
                res += 'Start time: %s\nEnd time: %s\n'%(self.starts[i][j], self.ends[i][j])
                timediff = float(self.ends[i][j]) - float(self.starts[i][j])
                res += 'Time taken: %4.2f seconds\n'%(timediff)
                print len(self.steps[i][j])
                res += 'Time per step: %4.2f seconds\n'%(timediff/len(self.steps[i][j]))
                res += '\n'
        print res

if __name__ == '__main__':
    TestParser()
