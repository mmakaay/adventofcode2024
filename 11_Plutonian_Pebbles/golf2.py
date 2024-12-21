from collections import Counter as C
A=C(input().split())
for _ in "x"*75:
 N=C()
 for n,c in A.items():
  l=len(n)
  if n=="0":N["1"]+=c
  elif l%2:N[str(int(n)*2024)]+=c
  else:l>>=1;N[n[:l]]+=c;N[str(int(n[l:]))]+=c
 A=N
print(A.total())
