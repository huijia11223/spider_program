import random

s=[]
for i in range(0,10):
    s.append(random.randint(1,1000))

for i in range(0,len(s)):
    print(s[i],end=",")
    
