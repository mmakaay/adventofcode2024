C={}
for a, b in[line.strip().split("-") for line in open(0)]:C.setdefault(a,set()).add(b);C.setdefault(b,set()).add(a)
print(sum(any(n[0]=="t"for n in t)for t in{tuple(sorted((a,b,c)))for a in C for b in C[a]for c in C[b]if a in C[c]and a!=c}))
