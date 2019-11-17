#p=2
#q=7

def getNumber(a,b): #소수를 찾자
    q=0
    r=0
    while(True):
        q=a/b
        r=a%b
        if r==0:
            break
        a=b
        b=r
    if b==1:
        return True
    else:
        return False



p=59
q=31



n=p*q
n1=(p-1)*(q-1)
f=True
i=2
while f:
    if getNumber(n1,i):
        f=False
    else:
        i+=1

e=i
m=25

f=True
i=2

#d를 찾자!(ed%(p-1)(q-1)==1을 만족해야한다.)
while f:
    if (e*i)%n1==1:
        break
    else:
        i+=1

d=i
print("p",p,"q",q)
print("n:",n)
print("(p-1)(q-1):",n1)
print("e:",e)
print("d:",d)

c=(m**e)%n

print("c:",c)
print("m:",m)
print((c**d)%n)


