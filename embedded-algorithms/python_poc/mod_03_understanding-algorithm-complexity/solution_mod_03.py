def dup_count_naive(a):
    c=0
    for i in range(len(a)):
        for j in range(i): c+= a[i]==a[j]
    return c
