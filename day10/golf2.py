M=[list(map(int,l.strip()))for l in open(0)]
W,H=len(M[0]),len(M)
def S(x,y,T=0):
 for X,Y in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=X<W and 0<=Y<H and M[Y][X]==M[y][x]+1:T=S(X,Y,T)
 return T+(M[y][x]>8)
print(sum(S(x,y)for y in range(H)for x in range(W)if M[y][x]<1))
