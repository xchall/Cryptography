
def nod(r1, r2, s1, s2, t1, t2):
    q = r1 // r2
    r = r1 - q * r2
    if r == 0:
        return s2, t2
    s = s1 - q * s2
    t = t1 - q * t2
    # print(r2, r, s2, s, t2, t)
    return nod(r2, r, s2, s, t2, t)


def nok_of_two(a, b) -> int:
    if a > b :
        s,t = nod(a, b,1,0,0,1)
        d = a * s + b * t
    else:
        s, t = nod(b, a, 1, 0, 0, 1)
        d = b * s + a * t
    return int((a * b) / d)


def nok(a):
    nk = a[0]
    for i in range(0,len(a)):
        if i > 0:
            nk = nok_of_two(a[i], nk)
            # print(nk)
    return nk

def proiz(a):
    pr = a[0]
    for i in range(1, len(a)):
        pr*= a[i]
    return pr

# функция эйлера
def euler(a):
    count = 1
    for i in range(2, a):
        s, t = nod(a, i, 1, 0, 0, 1)
        d = a * s + i * t
        if d == 1:
            count += 1
    return count

#проверка совместности системы
def check_system_compatibility(list_a: list, list_m: list) -> bool:
    for i in range(0, len(list_a)):
        for j in range(0, len(list_a)):
            if j!= i:
                if list_m[i] > list_m[j]:
                    s, t = nod(list_m[i], list_m[j], 1, 0, 0, 1)
                    d = list_m[i] * s + list_m[j] * t
                else:
                    s, t = nod(list_m[j], list_m[i], 1, 0, 0, 1)
                    d = list_m[j] * s + list_m[i] * t
                if (list_a[i] - list_a[j]) % d != 0: #по теореме
                    print(f"list_a[i] - list_a[j] = {list_a[i] - list_a[j]}  d = {d}")
                    return False #несовместна
    return True#совместна
#Китайская теорема об остатках

num = int(input("Enter number of equations in the system : "))

b = []
m = []
for i in range(num):
    bi = int(input(f"Enter  b{i+1} : "))
    mi = int(input(f"Enter  m{i+1} : "))
    b.append(bi % mi)
    m.append(mi)


M = nok(m)
if M == proiz(m):
    print("System has only 1 solution")
    # Находим Mi
    list_Mi = []
    list_Mli = []
    # Находим Mli
    for i in range(num):
        temp_m = m.copy()
        temp_m.pop(i)
        Mi = proiz(temp_m)
        list_Mi.append(Mi)
        Mli = pow(Mi, euler(m[i]) - 1) % m[i]
        list_Mli.append(Mli)
    print("M: ", M)
    print("Mi: ", list_Mi)
    print("Mli: ", list_Mli)
    x = 0
    for i in range(num):
        x += b[i] * list_Mi[i] * list_Mli[i]
    x0 = x % M
    print(f"Solution is x0 = {x0}")
else:
    #проверяем система совместна или нет

    #если совместна, то решаем сравнение первой степени
    if check_system_compatibility(b, m):
        print(f"System compatibility is True")
        #только для случая с 2 уравнениями (просто нужна реализация слияния уравнений во одно
        # m1*k = (b2-b1) (mod m2)
        # x = b1 + m1*k
        # решение сравнения первой степени

        if m[0] > m[1]:
            s, t = nod(m[0], m[1], 1, 0, 0, 1)
            d = m[0] * s + m[1] * t
        else:
            s, t = nod(m[1], m[0], 1, 0, 0, 1)
            d = m[1] * s + m[0] * t

        amount_of_solutions = d
        print(f"Amount of solutions = {amount_of_solutions} for {m[0]} * k = {(b[1]-b[0])%m[1]} (mod {m[1]})")

        # Сократим все сранение на d
        num_a = m[0]//amount_of_solutions
        num_b = ((b[1]-b[0]) % m[1])//amount_of_solutions
        num_m = m[1]//amount_of_solutions

        # по Теореме Эйлера
        ans0 = num_b * pow(num_a, euler(num_m) - 1)
        for i in range(0, amount_of_solutions):
            k = ans0 + i * num_m
            x = b[0] + m[0] * k
            print(f"Solution {i} = {x} ")
    else:
        print("System has no solutions")
