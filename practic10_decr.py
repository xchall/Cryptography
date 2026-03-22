# расширенный Евклид
def nod(r1, r2, s1, s2, t1, t2):
    q = r1 // r2
    r = r1 - q * r2
    if r == 0:
        return s2, t2
    s = s1 - q * s2
    t = t1 - q * t2
    return nod(r2, r, s2, s, t2, t)

def proiz(a):
    pr = a[0]
    for i in range(1, len(a)):
        pr *= a[i]
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

# CRT
def crt_two(b1, b2, m1, m2):
    print(f"{b1} mod {m1} and {b2} mod {m2}")
    b = [b1 % m1, b2 % m2]
    m = [m1, m2]

    M = proiz(m)

    # M1 и M2
    M1 = m2
    M2 = m1

    # обратные элементы через Эйлера
    M1_inv = pow(M1, euler(m1) - 1, m1)
    M2_inv = pow(M2, euler(m2) - 1, m2)

    x = (b[0] * M1 * M1_inv + b[1] * M2 * M2_inv) % M
    return x

# перевод в символ
def num_to_char(num):
    if 1 <= num <= 26:
        return chr(ord('A') + num - 1)
    elif num == 27:
        return ' '
    elif num == 28:
        return "'"
    elif num == 29:
        return '?'
    else:
        return '?'


def decrypt(cipher, p, q):
    result = []

    for c in cipher:
        print("______________")
        print(f"{c}")
        # корни по модулю p и q
        mp = pow(c, (p + 1) // 4, p)
        mq = pow(c, (q + 1) // 4, q)

        # 4 варианта через CRT
        r1 = crt_two(mp, mq, p, q)
        r2 = crt_two(mp, (-mq) % q, p, q)
        r3 = crt_two((-mp) % p, mq, p, q)
        r4 = crt_two((-mp) % p, (-mq) % q, p, q)
        print(r1, r2, r3, r4)
        result.append([r1, r2, r3, r4])

    return result


def main():
    p = int(input("Введите p: "))
    q = int(input("Введите q: "))

    cipher = list(map(int, input("Введите шифртекст (через пробел): ").split()))

    decrypted = decrypt(cipher, p, q)

    print("\nВарианты расшифровки:")

    for i, variants in enumerate(decrypted):
        chars = [num_to_char(v) for v in variants]
        print(f"{i+1}: {variants} -> {chars}")


if __name__ == "__main__":
    main()
