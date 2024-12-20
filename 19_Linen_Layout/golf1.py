from functools import*
I=open(0).read().split("\n")
P=[p.strip()for p in I[0].split(",")]
@cache
def C(d):return d=="" or any(d[:i]in P and C(d[i:])for i in range(len(d)+1))
print(sum(map(C,I[2:])))
