#!/usr/bin/env python3
import sys
from collections import Counter as C
A=C(next(sys.stdin).split())
for _ in range(75):
 N=C()
 for n,c in A.items():
  l=len(n)
  if n=="0":N["1"]+=c
  elif l%2<1:m=l//2;N[n[:m]]+=c;N[str(int(n[m:]))]+=c
  else:N[str(int(n)*2024)]+=c
 A=N
print(A.total())
