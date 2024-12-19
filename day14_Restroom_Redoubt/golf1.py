import re
R,K=[list(map(int,re.findall(r"-?\d+",l)))for l in open(0)],100
w,h=[1+max(r[i]for r in R)for i in[0,1]]
while K:=K-1:
 M,Q=[],[0]*5
 for x,y,v,u in R:M+=[[x:=(x+v)%w,y:=(y+u)%h,v,u]];R=M;Q[(y!=h//2)*(x!=w//2)*(1+(x>w//2)+(y>h//2)*2)]+=1
print(Q[1]*Q[2]*Q[3]*Q[4])
