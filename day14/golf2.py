import sys,re
w,h,t,R=101,103,0,[list(map(int,re.findall(r"-?\d+",line)))for line in sys.stdin]
while 1:
 M,O=[],set()
 for[x,y,v,u]in R:M+=[[x:=(x+v)%w,y:=(y+u)%h,v,u]];O.add((x,y))
 R,l=M,0;t+=1
 for y in range(h):
  for x in range(w):
   i=(x,y)in O;l=i*(l+i)
   if l>10:print(t);sys.exit()
