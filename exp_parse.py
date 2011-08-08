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
        test[1] = re.split('step \d+\n', test[1])
        print test
        print '\n\n'
        
if __name__ == '__main__':
    main()
