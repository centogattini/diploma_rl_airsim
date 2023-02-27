# 
from numpy import random, sqrt
def uniform():
    return random.uniform(0,1)
sample_size = 10000000
xs = [uniform() for i in range(sample_size)]
ys = [uniform() for i in range(sample_size)]
ans = 0
for i in range(sample_size):
    x, y = xs[i], ys[i]
    if sqrt((x-0.5)**2 + (y-0.5)**2) <= 0.5:
        ans += 1
print((ans/sample_size)/(0.5**2))