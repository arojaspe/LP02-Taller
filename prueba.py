from Simplex import Simplex
z = Simplex()
z.fo("fo max z  = "+str(10)+"*x1 + "+str(10)+"*x2 + "+str(15)+"*x3 ; r "+str(5)+"*x1 + "+str(2)+"*x2 + " +
     str(1)+"*x3 <= 10 "+str()+"; r "+str(2)+"*x1 + "+str(3)+"*x2 + "+str(9)+"*x3 >= 5 "+str()+"; } ")
print(z.x[3])

for i in range(0, 0, -1):
    x = y
    y = 10*z
    z = x+y
    print(x)
