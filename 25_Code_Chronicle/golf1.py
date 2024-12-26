K,L=[],[]
for b in open(0).read().split("\n\n"):
 R=b.splitlines()
 f=R[0][0]
 [L,K][f=="#"].append([sum(v)for v in list(zip(*[[c=="#"for c in l]for l in R[1:-1]]))])
print(sum(all(l+k<=5 for l,k in zip(v,u))for u in K for v in L))
