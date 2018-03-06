import time
a = time.time()
L = [3,23,5,7.888,0,9.1234,10.4566]
MM = sorted(L,reverse=True)[0]
b = time.time()
JJ = L[0] if 45>90 else L[-1]
c = time.time()
time.sleep(1)
d = time.time()
print(b-a,c-b,d-c)