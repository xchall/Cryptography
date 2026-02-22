
#Нахождение НОД расширенным алгоритмом Евклида
def nod(r1, r2, s1, s2, t1, t2):
    q = r1 // r2
    r = r1 - q * r2
    if r == 0:
        return s2, t2
    s = s1 - q * s2
    t = t1 - q * t2
    print(r2, r, s2, s, t2, t)
    return nod(r2, r, s2, s, t2, t)

#Частное решение диафантового уравнения

a = int(input("Enter a number a: "))
b = int(input("Enter a number b: "))
c = int(input("Enter a number c: "))

s,t = nod(a, b,1,0,0,1)

d = a * s + b * t

if c % d == 0:
    print("The equation has an infinite number of solutions")
else:
    print("The equation has no solutions")
    exit()

a1 = a // d
b1 = b // d
c1 = c // d

#найдем s и t в равенстве a1*s + b1*t = 1
s,t = nod(a1,b1,1,0,0,1)

x0 = (c/d) * s
y0 = (c/d) * t

print(f"Partial solution x0 = {x0} and y0 = {y0}")

#Общеее решение диафантового уравнения

print(f"General solution x = {x0} + k * {b/d} and y = {y0} - k * {a/d}, where k is integer")
