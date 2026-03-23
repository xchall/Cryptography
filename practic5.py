import math
from math import gcd
from itertools import combinations


# Проверка: является ли число гладким
def factor_over_base(n, base):
    exponents = []
    temp = n

    for p in base:
        count = 0
        while temp % p == 0:
            temp //= p
            count += 1
        exponents.append(count)

    if temp == 1:
        return exponents
    return None


# Проверка: является ли произведение квадратом
def is_square_exponents(exp_list):
    total = [0] * len(exp_list[0])

    for exps in exp_list:
        for i in range(len(exps)):
            total[i] += exps[i]

    return all(e % 2 == 0 for e in total), total
# all(...) сворачивает последовательность булевых значений в одно;
# хотя бы 1 false, всё false



# Строим X и Y
def build_X_Y(subset, total_exp, base):
    X = 1
    for x, _, _ in subset:
        X *= x

    Y = 1
    for p, e in zip(base, total_exp):
        Y *= p ** (e // 2)

    return X, Y



# квадратичное решето
def quadratic_sieve(n, factor_base):

    relations = []
    x = int(math.isqrt(n)) + 1

    while True:
        value = x * x - n

        exponents = factor_over_base(value, factor_base)

        if exponents is not None:
            print(f"[+] Гладкое число найдено: x={x}, x^2-n={value}")
            relations.append((x, value, exponents))

            # --- пытаемся найти зависимость ---
            for r in range(1, len(relations) + 1):
                for subset in combinations(relations, r):

                    exp_list = [rel[2] for rel in subset]
                    is_square, total_exp = is_square_exponents(exp_list)

                    if is_square:
                        print("\nНайдена зависимость")
                        for rel in subset:
                            print(f"  x={rel[0]}, value={rel[1]}, exps={rel[2]}")
                        print("total_exp:", total_exp)
                        print("factor_base:", factor_base)

                        X, Y = build_X_Y(subset, total_exp, factor_base)

                        factor = gcd(X - Y, n)

                        if factor != 1 and factor != n:
                            print(f"[+] Делитель найден: {factor}")
                            return factor, n // factor

        x += 1



if __name__ == "__main__":
    n = 1207
    factor_base = [2, 3, 5, 7, 11]

    print(f"Факторизация числа {n}")
    factors = quadratic_sieve(n, factor_base)
    print("\nРезультат:", factors)
