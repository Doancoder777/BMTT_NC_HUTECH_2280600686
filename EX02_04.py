j = []

a = int(input("Nhap a "))
b = int(input("Nhap b "))


for i in range(a,b):
    if(i%7 == 0 and i %5!=0):
        j.append(str(i))
print(",".join(j))