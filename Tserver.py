import socket
ip = "127.0.0.1"
port = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data.decode())
            if not data:
                break
            conn.sendall(b"pong")