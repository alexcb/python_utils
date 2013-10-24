#!/usr/bin/python
import sys
import time

start = time.time()

try:
    while 1:
        time_now = time.time()
        sys.stdout.write('\r%0.2f seconds elapsed' % (time_now - start,))
        sys.stdout.flush()
        time.sleep(0.01)
except KeyboardInterrupt:
    sys.stdout.write('\rTotal time: %0.2f seconds\n' % (time_now - start,))
    sys.stdout.flush()
