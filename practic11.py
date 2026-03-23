#MD6
#Вариант 10

import struct

# Параметры MD6
w = 64 # ширина слова в битах
r = 40 # количество раундов сжатия
n = 89  # размер внутреннего массива для блока
mod = 2 ** w


# Вращение
def rol(x, s):
    return ((x << s) | (x >> (w - s))) & (mod - 1)


# Константы
# Используются как начальные значения массива для компрессии.
Q = [
    0x7311c2812425cfa0, 0x6432286434aac8e7,
    0xb60450e9ef68b7c1, 0xe8fb23908d9f06f1,
    0xdd2e76cba691e5bf, 0x0cd0d63b2c30bc41,
    0x1f8ccf6823058f8a, 0x54e5ed5b88e3775d,
    0x4ad12aae0a6d6031, 0x3e7f16bb88222e0d,
    0x8af8671d3fb50c2c, 0x995ad1178bd25c31,
    0xc878c1dd04c4b633, 0x3b72066c7a1552ac,
    0x0d6f3522631effcb
]


# Padding
# дополнить сообщение так, чтобы его длина была кратна 512 битам (64 байта)
def pad(data):
    data = bytearray(data)
    bit_len = len(data) * 8

    data.append(0x80)
    while (len(data) % 64) != 56:
        data.append(0)

    data += struct.pack("<Q", bit_len)
    return data


# Компрессионная функция MD6 (упрощённая)
def md6_compress(block):
    words = list(struct.unpack("<8Q", block)) # 8 слов по 8 байт, в оригинале 16 слов по 8 байт

    A = Q + words + [0] * (n - len(Q) - len(words))

    for i in range(r): # раунды сжатия
        for j in range(16, n):
            x = A[j - 16] ^ A[j - 9]
            x ^= A[j - 3]
            x ^= A[j - 1]
            x ^= i

            A[j] = rol(x, (j + i) % 64)

    return A[-4:]  # 256 бит результат, 4 * 64
    #Берутся последние 4 слова массива


# Основная функция хеширования
def md6_hash(message):
    data = message.encode("utf-8")
    data = pad(data)

    result = []

    for i in range(0, len(data), 64):
        block = data[i:i + 64]
        compressed = md6_compress(block)
        result.extend(compressed)

    # итоговый хеш (hex)
    return ''.join(f"{x:016x}" for x in result)


# CLI интерфейс
def main():
    while True:
        print("\nВыберите действие:")
        print("1 — Хешировать (MD6)")
        print("0 — Выход")

        choice = input(">> ")

        if choice == "1":
            text = input("Введите текст: ")
            hashed = md6_hash(text)
            print("MD6 хеш:")
            print(hashed)

        elif choice == "0":
            break

        else:
            print("Неверный ввод!")


if __name__ == "__main__":
    main()
