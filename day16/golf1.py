#!/usr/bin/env python3
import sys,heapq as h
from collections import defaultdict as d
def E(x,y,p,d):c=C[y][x][p];C[(c<0 or d<c)*y][x][p]=d;h.heappush(Q,(d,x,y,p))
M,Q,C=[list(l.strip())for l in sys.stdin],[],d(lambda:d(lambda:[-1]*4));E(1,len(M)-2,1,0)
while Q:
 c,x,y,e=h.heappop(Q)
 if(x,y)==(len(M[0])-2,1):print(c);break
 l,m=[(0,-1),(1,0),(0,1),(-1,0)][e];j,k=x+l,y+m
 if not M[k][j]=="#":g=c+1;E(j,k,e,g)
 for r in(-1, +1):E(x,y,(e+r)%4,c+1000)
