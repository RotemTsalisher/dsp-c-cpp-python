def popcount(x):
    c=0
    while x: x&=x-1; c+=1
    return c
