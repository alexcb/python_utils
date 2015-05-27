#!/usr/bin/python

import fileinput
import sys

num_lines = 0
try:
    for line in fileinput.input():
        num_lines += 1
    
        sys.stdout.write('\rtotal lines: %s' % (num_lines,))
        sys.stdout.flush()
except KeyboardInterrupt:
    pass

sys.stdout.write('\rtotal lines: %s\n' % (num_lines,))

