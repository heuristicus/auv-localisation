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
        tests.append(re.split('newtest\n', conf))
        splitsteps = []
    for test in tests:
        for num in map(lambda x: x + 1, range(len(test[1:]))):
            test[num] = re.split('step \d+\n', test[num])
            for step in range(len(test[num])):
                test[num][step] = test[num][step].split('\n')[:-1]
        
    for test in tests[0]:
        print test
if __name__ == '__main__':
    main()
