def activity_sel(start,finish):
    idx=sorted(range(len(finish)), key=lambda i: finish[i])
    pick=[]; last=-1
    for i in idx:
        if start[i]>=last: pick.append(i); last=finish[i]
    return pick
