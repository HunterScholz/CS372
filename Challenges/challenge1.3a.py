import socket

s = socket.socket()

server = ("localhost", 2222)
s.connect(server)

data = s.recv(100)
str = data.decode(errors="ignore")
print(str)
