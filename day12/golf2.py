#!/usr/bin/env python3
import sys
P=[list(l.strip())for l in sys.stdin]
w,h,S,T=len(P[0]),len(P),set(),0
def i(x,y,r):
 S.add((x,y));r[0]+=1
 for m,n in[(-1,-1),(1,-1),(1,1),(-1,1)]:s,b,d=E(x,y,x+m,y),E(x,y,x,y+n),E(x,y,x+m,y+n);r[1]+=s and b and not d or not(s or b)
 for m,n in[(-1,0),(0,-1),(1,0),(0,1)]:m,n=x+m,y+n;E(x,y,m,n)and(m,n)not in S and i(m,n,r)
 return r[0]*r[1]
def E(x,y,m,n):return 0<=m<w and 0<=n<h and P[y][x]==P[n][m]
print(sum(i(x,y,[0,0])for y in range(h)for x in range(w)if(x,y)not in S))
