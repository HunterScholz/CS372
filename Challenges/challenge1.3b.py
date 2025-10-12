import socket

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 2222))
s.listen()

while True:
    client_socket, client_addr = s.accept()
    print(client_addr)
    client_socket.sendall("Some data!\n".encode())
    client_socket.close()