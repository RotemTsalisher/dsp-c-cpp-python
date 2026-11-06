def window_max(a,k):
    if k<1: raise ValueError
    from collections import deque
    dq=deque(); out=[]
    for i,x in enumerate(a):
        while dq and dq[0]<=i-k: dq.popleft()
        while dq and a[dq[-1]]<=x: dq.pop()
        dq.append(i)
        if i>=k-1: out.append(a[dq[0]])
    return out
