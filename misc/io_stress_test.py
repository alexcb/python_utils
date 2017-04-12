import os
import random
import time

def write(filename,data,offset):
    try:
        f = open(filename,'r+b')
    except IOError:
        f = open(filename,'wb')
    f.seek(offset)
    f.write(data)
    f.close()

def read(filename, size, offset):
    with open(filename, 'r') as f:
        f.seek(offset)
        while size > 0:
            x = f.read(1024)
            size -= len(x)
            if not x:
                break

path = '/tmp/randdata'
size = 1024 * 1024
times = 30000

while 1:

    start = time.time()
    print 'writting'
    for _ in xrange(times):
        ch = chr(random.randint(50,60))
        offset = random.randint(1,1024*1024*1024*5)
        write(path, ch * size, offset)
    print 'reading'
    write_duration = time.time() - start
    start = time.time()
    for _ in xrange(times):
        offset = random.randint(1,1024*1024*1024*5)
        read(path, size, offset)
    read_duration = time.time() - start
    duration = read_duration + write_duration
    print 'write took %s seconds; read took %s seconds; sleeping for %s seconds' % (write_duration, read_duration, duration)
    time.sleep(duration)

