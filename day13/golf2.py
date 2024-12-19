import re
T,f=0,open(0)
try:
 while p:=[int(x)+o for o in[0,0,10**13]for x in re.findall(r"\d+",next(f))]:
  [A,B,C,D,E,F]=p;H=(F*C-E*D)//(B*C-A*D);I=(E-H*A)//C
  T+=(H*I>=0)*(H*A+I*C==E)*(H*B+I*D==F)*(H*3+I);next(f)
except:0
print(T)
