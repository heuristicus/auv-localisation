#!/usr/bin/python
import sys
import re

def main():
    """
    """
    f = open(sys.argv[1])
    data = f.read()
    
    # split each test to a separate list, ignoring the blank
    confs = data.split('newconf\n')[1:] 
    #for item in confs:
    #    print [item]
    #    print '\n\n\n'
    #return
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
            end = item[-1] if item[-1] is not '' else item[-2]
            t_end.append(end[0].split(' ')[1])
            start = item[0][1].split(' ')[1]
            t_start.append(start)
            step = item[1]
            t_step.append(step)
        steps.append(t_step)
        ends.append(t_end)
        starts.append(t_start)
    print steps
    #print ends
    #print starts
    #print confs
        
if __name__ == '__main__':
    main()
