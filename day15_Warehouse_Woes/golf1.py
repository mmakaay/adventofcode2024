n,W,P,R=enumerate,[],"",0
for y,l in n(open(0)):
 if l[0]=="#":r=list(l);W+=[r];R=(r.index("@"),y)if"@"in r else R
 else:P+=l.strip()
for D in P:
 b,P,(x,y),(v,w)="@",[],R,{"<":(-1,0),">":(1,0),"^":(0,-1),"v":(0,1)}[D];P+=[R]
 while b in"@O":x+=v;y+=w;P+=[(x,y)];b=W[y][x];P*=b!="#"
 for i,(x,y)in n(P):W[y][x]=".@O"[min(i,2)];R=[R,(x,y)][i==1]
print(sum(x+100*y for y,r in n(W)for x,e in n(r)if e=="O"))
