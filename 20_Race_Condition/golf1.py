F,c,t,M="X"*4,0,0,[list(line.strip())for line in open(0)];w,h=len(M[0]),len(M)
x,y=next((x,y)for y in range(h)for x in range(w)if M[y][x]=="S")
T={(x,y):t}
while M[y][x]!="E":
 a,b=0,-1
 for _ in F:
  a,b=-b,a;v,u=x+a,y+b
  if(v,u)not in T and M[u][v]!="#":t+=1;T[(v,u)]=t;x,y=v,u
for (x,y),S in T.items():
 a,b=0,-1
 for _ in F:
  a,b=-b,a;v,u=x+a,y+b;e,f=v+a,u+b
  if M[u][v]=="#" and 0<e<w and 0<f<h and M[f][e]!="#":c+=T[(e,f)]-S-2>=100
print(c)
