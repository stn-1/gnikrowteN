import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# ===== AES HELPERS =====
def encrypt(key, msg):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())

    return base64.b64encode(cipher.nonce + tag + ciphertext)

def decrypt(key, data):
    raw = base64.b64decode(data)

    nonce = raw[:16]
    tag = raw[16:32]
    ciphertext = raw[32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# ===== CLIENT =====
#aes_key = get_random_bytes(16)  # 🔑 shared key (demo)
aes_key = b'MySecretKey12345'   #example
def receive(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break

            try:
                msg = decrypt(aes_key, data)
                print(f"\n👤 {msg}\nyou: ", end="")
            except:
                print("\n[can't decrypt]")

        except:
            break

def send(sock):
    while True:
        msg = input("you: ")

        if msg.lower() == "exit":
            break

        enc = encrypt(aes_key, msg)
        sock.send(enc)

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(("127.0.0.1", 8080))

    print("[CONNECTED]")

    threading.Thread(target=receive, args=(s,), daemon=True).start()
    send(s)

    s.close()

if __name__ == "__main__":
    start_client()