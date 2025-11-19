# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    listen_socket = socket.socket()
    listen_socket.bind(('127.0.0.1', port))
    listen_socket.listen()
    read_set = {listen_socket}

    while read_set:
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for s in ready_to_read:
            if s is listen_socket:
                new_s, _ = s.accept()
                read_set.add(new_s)
                h, p = new_s.getpeername()
                print(f"({h}, {p}): connected")
            else:
                h, p = s.getpeername()
                data = s.recv(4096)
                if data:
                    data_len = len(data)
                    print(f"({h}, {p}) {data_len} bytes: {data}")
                else:
                    print(f"({h}, {p}): disconnected")
                    read_set.remove(s)
                    #s.close()
    pass

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
