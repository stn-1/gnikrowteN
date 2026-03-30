import socket
import os


BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def start_server(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip,port))
    s.listen(1)

    print(f"Wait client send file at: {ip} {port}")

    conn,addr=s.accept()
    print("connected")
    #colect infomation about file
    received=conn.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    #name file and change file size to int
    filename=os.path.basename(filename)
    filesize=int(filesize)

    # state 2: receive file
    print(f"receive file {filename} size: {filesize}")

    with open(f"receive_{filename}","wb") as f:
        byte_received=0
        while byte_received<filesize:
            bytes_read=conn.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            byte_received+=bytes_read
    print(f"save successful {filename}")
    conn.close()
    s.close()

def start_client(ip,port,file_path):
    if not os.path.exists(path):
        print("file not exist")
        return
    filesize = os.path.getsize(file_path)
    filename = os.path.basename(file_path)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.connect((ip,port))
        print("connect to server")
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        print("loading...")
        with open(file_path,"rb") as f:
            while True:
                bytes_read=f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
        print("send file completed.")
    except Exception as e:
        print(f"err:{e}")
    finally:
        s.close()


if __name__ == "__main__":
    choice = input("Choose (1: Server - Receive file, 2: Client - Send file) ")
    IP = "127.0.0.1"
    PORT = 8080

    if choice == "1":
        start_server(IP, PORT)
    else:
        path = input("enter file path: ")
        start_client(IP, PORT, path)