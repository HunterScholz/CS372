import socket
import time

def system_seconds_since_1900():
    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

s = socket.socket()
server = ("time.nist.gov", 37)
s.connect(server)

data = s.recv(4096)
s.close()
nist_time = int.from_bytes(data, 'big')

print("NIST time : " + str(nist_time))
print("System time : " + str(system_seconds_since_1900()))