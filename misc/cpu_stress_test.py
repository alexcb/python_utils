import time

def make_pi(n):
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    ppp = []
    while len(ppp) < n:
        if 4 * q + r - t < m * t:
            ppp.append(m)
            q, r, t, k, m, x = (10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x)
        else:
            q, r, t, k, m, x = (q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2)
    return ppp

def fib(num):
    a = 0
    b = 1
    while b <= num:
        prev_a = a
        a = b
        b = prev_a +b
        #print b                                                                                                          
    return a


while 1:
   print 'start'
   print make_pi(100000)
   time.sleep(60)
