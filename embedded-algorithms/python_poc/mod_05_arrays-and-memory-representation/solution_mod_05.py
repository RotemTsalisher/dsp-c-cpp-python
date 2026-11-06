def insert_at(a,n,x,i):
    if n>=len(a): raise ValueError
    for j in range(n,i,-1): a[j]=a[j-1]
    a[i]=x
    return n+1
