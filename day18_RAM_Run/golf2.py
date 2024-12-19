from heapq import heappush as I, heappop as O
def X(n):
 w,h=[1+max(v[i]for v in M)for i in[0, 1]]
 S,E,D,Q,C=(0,0),(w-1,h-1),[(0,-1),(1,0),(0,1),(-1,0)],[],{};C[S]=0;I(Q,(0,S))
 while Q:
  c,(x,y)=O(Q)
  if (x,y)==E:return c
  for f,g in D:
   j,k=x+f,y+g;d=c+1;s=(j,k)
   if 0<=j<w and 0<=k<h and not(j,k)in M[:n]and(d<C.get(s,w*h)):C[s]=d;I(Q,(d,s))
M=[tuple(map(int,l.strip().split(",")))for l in open(0)];L,U=0,len(M);A=0
while True:
 P=L+(U-L)//2
 if P==A:print(M[U-1]);break
 A=P
 if X(P):L=P
 else:U=P
