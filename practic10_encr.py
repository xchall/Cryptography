#Алгоритм Рабина
#Шифруем

# Iron Man
# What`s going on?

# --- СЛОВАРЬ ---
def char_to_num(ch):
    ch = ch.upper()

    if 'A' <= ch <= 'Z':
        return ord(ch) - ord('A') + 1
    elif ch == ' ':
        return 27
    elif ch == "`":
        return 28
    elif ch == '?':
        return 29
    else:
        raise ValueError(f"Недопустимый символ: {ch}")

# --- ШИФРОВАНИЕ ---
def encrypt(message, n):
    result = []

    for ch in message:
        m = char_to_num(ch)
        c = (m * m) % n
        result.append(c)

    return result

# --- MAIN ---
def main():
    n = int(input("Введите открытый ключ (n): "))
    message = input("Введите сообщение: ")

    encrypted = encrypt(message, n)

    print("Зашифрованное сообщение:")
    print(" ".join(map(str, encrypted)))

if __name__ == "__main__":
    main()
