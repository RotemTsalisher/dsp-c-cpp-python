def dc_max(a,lo,hi):
    if lo==hi: return a[lo]
    mid=(lo+hi)//2
    return max(dc_max(a,lo,mid), dc_max(a,mid+1,hi))
