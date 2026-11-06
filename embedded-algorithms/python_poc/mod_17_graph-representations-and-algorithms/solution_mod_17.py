def bfs(adj,s):
    seen={s}; q=[s]; order=[]
    while q:
        u=q.pop(0); order.append(u)
        for v in adj.get(u,()):
            if v not in seen: seen.add(v); q.append(v)
    return order
