def array_stats(v):
    return max(v), min(v), sum(v)/len(v), sum(1 for x in v if x==v[0])
