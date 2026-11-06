def running_rms(chunks):
    sq=0; n=0
    for ch in chunks:
        for x in ch: sq+=x*x; n+=1
        yield (sq/n)**0.5 if n else 0.0
