import socket

s = socket.socket()

server = ("flip.engr.oregonstate.edu", 2187)
s.connect(server)

while True:
    data = s.recv(100)
    str = data.decode(errors="ignore")
    print(str, end='')
