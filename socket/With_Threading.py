import socket
import threading

clients = []
clients_lock = threading.Lock() # Khóa để đảm bảo an toàn giữa các thread

def broadcast(msg, current_conn):
    # Thu thập client lỗi để xóa sau, tránh deadlock
    failed_clients = []
    with clients_lock:
        for client in clients[:]:
            if client != current_conn:
                try:
                    client.send(msg)
                except Exception as e:
                    print(f"[LỖI BROADCAST] {e}")
                    failed_clients.append(client)
    # Xóa client lỗi SAU KHI đã giải phóng lock
    for client in failed_clients:
        remove_client(client)

def remove_client(conn):
    with clients_lock:
        if conn in clients:
            clients.remove(conn)
            conn.close()

def handle_client(conn, addr):
    print(f"[HỆ THỐNG] Kết nối mới: {addr}")
    with clients_lock:
        clients.append(conn)

    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break

            decode_msg = msg.decode("utf-8")
            if decode_msg.lower() == "exit":
                break

            print(f"[{addr}]: {decode_msg}")
            broadcast(f"Người lạ: {decode_msg}".encode("utf-8"), conn)
        except Exception as e:
            print(f"[LỖI HANDLE_CLIENT] {addr}: {e}")
            break

    print(f"[HỆ THỐNG] {addr} đã thoát")
    remove_client(conn)

def start_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Cho phép dùng lại port ngay lập tức
    try:
        s.bind((ip, port))
        s.listen(5)
        print(f"[SERVER] Đang chạy tại {ip}:{port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True # Thread con sẽ tự đóng khi thread chính đóng
            thread.start()
    except Exception as e:
        print(f"[LỖI SERVER]: {e}")
    finally:
        s.close()

# --- CLIENT ---
def client_receive(s):
    while True:
        try:
            msg = s.recv(1024).decode('utf-8')
            if not msg:
                break
            # Xóa dòng hiện tại và in tin nhắn mới, sau đó in lại prompt
            print(f"\rTin nhắn mới: {msg}\nyou: ", end="")
        except Exception as e:
            print(f"[LỖI CLIENT_RECV] {e}")
            break

def client_send(s):
    while True:
        try:
            msg = input("you: ")
            s.send(msg.encode("utf-8"))
            if msg.lower() == "exit":
                break
        except Exception as e:
            print(f"[LỖI CLIENT_SEND] {e}")
            break

def start_client(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        print(f"Đã kết nối tới server {ip}:{port}")

        t_recv = threading.Thread(target=client_receive, args=(s,))
        t_send = threading.Thread(target=client_send, args=(s,))

        t_recv.daemon = True # Quan trọng: để thread nhận đóng khi thread gửi đóng
        t_recv.start()
        t_send.start()

        t_send.join() # Chờ người dùng gõ "exit"
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
    finally:
        s.close()
        print("Đã ngắt kết nối.")

if __name__ == "__main__":
    choice = input("Chọn chế độ (1: Server, 0: Client): ")
    if choice == "1":
        start_server("127.0.0.1", 8080)
    else:
        start_client("127.0.0.1", 8080)