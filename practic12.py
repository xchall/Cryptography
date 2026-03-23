import gostcrypto
from gostcrypto import gosthash, gostsignature
import secrets

# --- Сообщение для подписи ---
message = "Тестовая строка для подписи".encode("utf-8")

# --- Хеш со Streebog‑256 ---
hobj = gosthash.new("streebog256", data=message)
digest = hobj.digest()
print("Digest (Streebog256):", digest.hex())

# --- Инициализация объекта подписи (256‑бит) и выбор кривой ---
sign_obj = gostsignature.new(
    gostsignature.MODE_256,
    gostsignature.CURVES_R_1323565_1_024_2019["id-tc26-gost-3410-2012-256-paramSetB"]
)

# --- Случайный приватный ключ 32 байта ---
private_key = bytearray(secrets.token_bytes(32))
print("Private key:", private_key.hex())

# --- Генерация публичного ключа ---
public_key = sign_obj.public_key_generate(private_key)
print("Public key:", public_key.hex())

# --- Подпись сообщения ---
signature = sign_obj.sign(private_key, digest)
print("Signature:", signature.hex())

# --- Проверка подписи ---
is_valid = sign_obj.verify(public_key, digest, signature)
print("Подпись верна?", is_valid)
