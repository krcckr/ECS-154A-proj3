import socket
ip = "127.0.0.1"
port = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip,port))
    s.sendall("ping".encode())
    data = s.recv(1024)
    print(data.decode())

