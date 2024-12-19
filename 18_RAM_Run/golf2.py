from heapq import*
M=[tuple(map(int,l.split(',')))for l in open(0)]
def f(n):
 S=M[:n];w=max(a[0]for a in M)+1;h=max(a[1]for a in M)+1;Q=[(0,(0,0))];D,r,t={(0,0):0},0,-1
 while Q:
  c,(x,y)=heappop(Q);i=5
  if(x,y)==(w-1,h-1):return c
  while i:=i-1:
   r,t=-t,r;X,Y=x+r,y+t;d=c+1;s=(X,Y)
   if 0<=X<w and 0<=Y<h and s not in S and d<D.get(s,w*h):D[s]=d;heappush(Q,(d,s))
L,U,A,P=0,len(M),0,0
while U!=A:
 P=(L+U)//2;A=P
 if f(P):L=P
 else:U=P
print(M[U-1])
