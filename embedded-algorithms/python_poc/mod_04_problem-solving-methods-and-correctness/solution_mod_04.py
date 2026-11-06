def is_sorted(a):
    return all(a[i]<=a[i+1] for i in range(len(a)-1))
