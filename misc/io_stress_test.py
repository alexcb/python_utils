import os
import random
def write(filename,data,offset):
    try:
        f = open(filename,'r+b')
    except IOError:
        f = open(filename,'wb')
    f.seek(offset)
    f.write(data)
    f.close()

while 1:
    ch = chr(random.randint(50,60))
    size = random.randint(1,1024*10)
    offset = random.randint(1,1024*1024*1024*5)
    write('/tmp/randdata', ch * size, offset)

