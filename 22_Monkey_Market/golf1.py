T,p=0,2**24
for s in map(int,open(0)):
 for _ in range(2000):s^=s<<6&p;s^=s>>5;s^=s<<11&p
 T+=s
print(T)
