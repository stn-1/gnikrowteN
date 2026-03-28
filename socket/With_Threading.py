import socket
import threading


#server handler
def server_send(conn):
    while True:
        try:
            msg=input()
            conn.send(msg.encode('utf-8'))
            if msg=="exit":
                break
        except:
            break


def server_recv(conn):
    while True:
        try:
            msg=conn.recv(1024).decode('utf-8')
            if not msg or msg=="exit":
                print("server out")
                break
            print(f"\nsomeone: { msg} ")
        except:
            break


def start_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(1)
    print(f"server {ip}:{port}...")

    conn,addr=s.accept()
    print(f"connet by {addr}")

    #creat theard
    t_send=threading.Thread(target=server_send,args=(conn,))
    t_recv=threading.Thread(target=server_recv,args=(conn,))

    t_send.start()
    t_recv.start()

    t_send.join()
    conn.close()


#client handler
def client_receive(s):
    while True:
        try:
            msg=s.recv(1024).decode('utf-8')
            if not msg or msg=="exit":
                print("server disconnect")
                break
            print(f"\nserver send: {msg}")
        except:
            break


def client_send(s):
    while True:
        try:
            msg=input("you: ")
            s.send(msg.encode("utf-8"))
            if msg =="exit":
                break
        except:
            break


def start_client(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        print(f"Connect to server {ip}:{port}")

        t_recv = threading.Thread(target=client_receive, args=(s,))
        t_send = threading.Thread(target=client_send, args=(s,))

        t_recv.start()
        t_send.start()

        t_send.join()
    except Exception as e:
        print(f"fail to connect: {e}")
    finally:
        s.close()


# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    choice = input("1 or 0: ")

    if choice == "1":
        start_server("127.0.0.1", 8080)
    else:
        start_client("127.0.0.1", 8080)