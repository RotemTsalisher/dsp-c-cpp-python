class Stack:
    def __init__(self,cap): self.a=[0]*cap; self.n=0
    def push(self,x):
        if self.n>=len(self.a): raise OverflowError
        self.a[self.n]=x; self.n+=1
