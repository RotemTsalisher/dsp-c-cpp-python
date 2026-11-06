def c_strlen(s,maxlen):
    n=0
    while n<maxlen and s[n]: n+=1
    return n
