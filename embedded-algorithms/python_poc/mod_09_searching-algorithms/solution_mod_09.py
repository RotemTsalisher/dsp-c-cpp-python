def binary_search(a,t):
    lo,hi=0,len(a)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if a[mid]==t: return mid
        if a[mid]<t: lo=mid+1
        else: hi=mid-1
    return -1
