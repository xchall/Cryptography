#Вариант 10

import os
import struct

# Параметры RC6
w = 32
r = 20
mod = 2 ** w
Pw = 0xB7E15163
Qw = 0x9E3779B9


# Вспомогательные функции
def rol(x, y):
    return ((x << (y & 31)) | (x >> (32 - (y & 31)))) % mod


def ror(x, y):
    return ((x >> (y & 31)) | (x << (32 - (y & 31)))) % mod


# Генерация ключа
def generate_key(length=16): #создаёт 16 байт = 128 бит случайного ключа
    return os.urandom(length)


# Сохранение ключа
def save_key(key, filename="rc6_key.bin"):
    with open(filename, "wb") as f:
        f.write(key)


# Загрузка ключа
def load_key(filename="rc6_key.bin"):
    with open(filename, "rb") as f:
        return f.read()


# Расширение ключа
def key_expansion(key):
    b = len(key)
    u = w // 8
    c = max(1, b // u)

    L = [0] * c
    for i in range(b - 1, -1, -1):
        L[i // u] = (L[i // u] << 8) + key[i]

    t = 2 * (r + 2)
    S = [0] * t
    S[0] = Pw
    for i in range(1, t):
        S[i] = (S[i - 1] + Qw) % mod

    A = B = i = j = 0
    for _ in range(3 * max(c, t)):
        A = S[i] = rol((S[i] + A + B) % mod, 3)
        B = L[j] = rol((L[j] + A + B) % mod, (A + B))
        i = (i + 1) % t
        j = (j + 1) % c

    return S


# Шифрование блока (16 байт)
def encrypt_block(block, S):
    A, B, C, D = struct.unpack("<4I", block)

    B = (B + S[0]) % mod
    D = (D + S[1]) % mod

    for i in range(1, r + 1):
        t = rol(B * (2 * B + 1) % mod, 5)
        u = rol(D * (2 * D + 1) % mod, 5)

        A = (rol(A ^ t, u) + S[2 * i]) % mod
        C = (rol(C ^ u, t) + S[2 * i + 1]) % mod

        A, B, C, D = B, C, D, A

    A = (A + S[2 * r + 2]) % mod
    C = (C + S[2 * r + 3]) % mod

    return struct.pack("<4I", A, B, C, D)


# Расшифрование блока
def decrypt_block(block, S):
    A, B, C, D = struct.unpack("<4I", block)

    C = (C - S[2 * r + 3]) % mod
    A = (A - S[2 * r + 2]) % mod

    for i in range(r, 0, -1):
        A, B, C, D = D, A, B, C

        u = rol(D * (2 * D + 1) % mod, 5)
        t = rol(B * (2 * B + 1) % mod, 5)

        C = ror((C - S[2 * i + 1]) % mod, t) ^ u
        A = ror((A - S[2 * i]) % mod, u) ^ t

    D = (D - S[1]) % mod
    B = (B - S[0]) % mod

    return struct.pack("<4I", A, B, C, D)


# Дополнение (padding)
def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)


def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]


# Шифрование текста
def encrypt(text, S):
    data = text.encode("utf-8")
    data = pad(data)

    result = b""
    for i in range(0, len(data), 16):
        result += encrypt_block(data[i:i + 16], S)

    return result.hex()


# Расшифрование
def decrypt(hex_text, S):
    data = bytes.fromhex(hex_text)

    result = b""
    for i in range(0, len(data), 16):
        result += decrypt_block(data[i:i + 16], S)

    result = unpad(result)
    return result.decode("utf-8")



def main():
    key_file = "rc6_key.bin"

    if not os.path.exists(key_file):
        key = generate_key()
        save_key(key, key_file)
        print("Ключ сгенерирован и сохранён.")
    else:
        key = load_key(key_file)
        print("Ключ загружен из файла.")

    S = key_expansion(key)

    while True:
        print("\nВыберите действие:")
        print("1 — Шифровать")
        print("2 — Расшифровать")
        print("0 — Выход")

        choice = input(">> ")

        if choice == "1":
            text = input("Введите текст: ")
            encrypted = encrypt(text, S)
            print("Зашифрованный текст:")
            print(encrypted)

        elif choice == "2":
            text = input("Введите шифртекст (hex): ")
            try:
                decrypted = decrypt(text, S)
                print("Расшифрованный текст:")
                print(decrypted)
            except:
                print("Ошибка расшифровки!")

        elif choice == "0":
            break

        else:
            print("Неверный ввод!")


if __name__ == "__main__":
    main()
