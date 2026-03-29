import socket
import threading

clients = []
lock = threading.Lock()

def broadcast(msg, current_conn):
    with lock:
        for client in clients[:]:
            if client != current_conn:
                try:
                    client.send(msg)
                except:
                    clients.remove(client)
                    client.close()

def handle_client(conn, addr):
    print(f"[CONNECT] {addr}")

    with lock:
        clients.append(conn)

    try:
        while True:
            msg = conn.recv(4096)
            if not msg:
                break

            broadcast(msg, conn)

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    print(f"[DISCONNECT] {addr}")
    with lock:
        clients.remove(conn)
    conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 8080))
    s.listen(5)

    print("[SERVER] Running at 127.0.0.1:8080")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()