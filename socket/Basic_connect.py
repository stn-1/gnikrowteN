import socket

def listen(ip,port):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip,port))
    s.listen(1)
    conn,addr=s.accept()
    print("connected")
    while True:
        msg=input()
        conn.send(msg.encode())
        if msg=="exit":
            break
    conn.close()

def send(ip,port):
    s=socket.socket()
    s.connect((ip,port))
    while True:
        msg = s.recv(1024).decode()
        print(f"Server gửi: {msg}")
        if not msg: break



if __name__=="__main__":
    choice = input("0 or 1")

    if choice == "1":
        listen("127.0.0.1", 8080)
    else:
        send("127.0.0.1", 8080)
