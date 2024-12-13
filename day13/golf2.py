#!/usr/bin/env python3
import re,sys
T=0
try:
 while p:=[int(x)+o for o in[0,0,10**13]for x in re.findall(r"\d+",next(sys.stdin))]:
  [A,B,C,D,E,F]=p;H=(F*C-E*D)//(B*C-A*D);I=(E-H*A)//C
  T+=(H*I>=0)*(H*A+I*C==E)*(H*B+I*D==F)*(H*3+I);next(sys.stdin)
except:0
print(T)
