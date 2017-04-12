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
    for _ in xrange(times):
        offset = random.randint(1,1024*1024*1024*5)
        read(path, offset)
    duration = time.time() - start
    print 'IO task took %s seconds; sleeping for the same amount of time now' % duration
    time.sleep(duration)

