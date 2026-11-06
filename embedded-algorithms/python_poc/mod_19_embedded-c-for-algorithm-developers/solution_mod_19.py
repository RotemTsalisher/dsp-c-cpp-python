def sat_add16(a,b):
    s=a+b
    return 32767 if s>32767 else (-32768 if s<-32768 else s)
